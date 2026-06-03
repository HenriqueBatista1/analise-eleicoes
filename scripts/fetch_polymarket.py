import os
import sys
import json
import requests
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add scripts directory to path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from models import Base, PolymarketProbability
from constants import ELECTION_EVENT_ID

def fetch_markets():
    """
    Fetches the specific election event by ID and returns its associated markets.
    """
    url = f"https://gamma-api.polymarket.com/events/{ELECTION_EVENT_ID}"

    try:
        print(f"Querying Polymarket API for Event ID {ELECTION_EVENT_ID}...")
        response = requests.get(url)
        response.raise_for_status()
        event_data = response.json()

        markets = event_data.get("markets", [])
        return markets
    except Exception as e:
        print(f"Error fetching data for Event ID {ELECTION_EVENT_ID}: {e}")
        return []

def parse_and_save_markets(markets, session) -> int:
    """
    Fetches the complete historical price series for each candidate's market
    and persists new records to the database, preventing duplicates.
    """
    saved_count = 0

    if not markets:
        print("Warning: No markets found in the election event.")
        return 0

    print(f"Processing {len(markets)} markets from the election event...")

    # Load existing records in memory to prevent duplicate insertions
    try:
        existing_records = set(
            session.query(PolymarketProbability.market_id, PolymarketProbability.timestamp).all()
        )
        print(f"Loaded {len(existing_records)} existing records from the database.")
    except Exception as e:
        print(f"Error loading existing database records: {e}")
        existing_records = set()

    for m in markets:
        market_id = str(m.get("id", ""))
        candidate = m.get("groupItemTitle")

        if not candidate:
            continue

        # Skip placeholder outcomes
        candidate_lower = candidate.lower()
        if "person " in candidate_lower or "another person" in candidate_lower:
            continue

        clob_tokens_raw = m.get("clobTokenIds")
        if not clob_tokens_raw:
            continue

        try:
            # Handle potential double-encoded JSON strings from the API
            if isinstance(clob_tokens_raw, str):
                clob_tokens = json.loads(clob_tokens_raw)
            else:
                clob_tokens = clob_tokens_raw

            if not clob_tokens or len(clob_tokens) == 0:
                continue

            # The first token corresponds to the "Yes" outcome (the victory probability)
            yes_token_id = clob_tokens[0]

            # Fetch historical daily prices using interval="max"
            history_url = "https://clob.polymarket.com/prices-history"
            params = {
                "market": yes_token_id,
                "interval": "max"
            }

            response = requests.get(history_url, params=params)

            if response.status_code == 200:
                history_data = response.json()
                points = []
                if isinstance(history_data, list):
                    points = history_data
                elif isinstance(history_data, dict):
                    points = history_data.get("history", [])

                candidate_saved_count = 0
                for pt in points:
                    t_sec = pt.get("t")
                    price = pt.get("p")

                    if t_sec is None or price is None:
                        continue

                    db_timestamp = datetime.utcfromtimestamp(t_sec)

                    # Prevent duplicate insertions
                    if (market_id, db_timestamp) in existing_records:
                        continue

                    record = PolymarketProbability(
                        candidate_name=candidate,
                        probability=float(price),
                        timestamp=db_timestamp,
                        market_id=market_id
                    )

                    session.add(record)
                    candidate_saved_count += 1
                    saved_count += 1

                    # Update local set to prevent duplicates within the same execution loop
                    existing_records.add((market_id, db_timestamp))

                print(f"-> Candidate: {candidate} | Fetched: {len(points)} | Saved: {candidate_saved_count} new records")
            else:
                print(f"-> Candidate: {candidate} | Failed to fetch price history: HTTP {response.status_code}")

        except Exception as e:
            print(f"Error processing price history for market ID {market_id} ({candidate}): {e}")
            continue

    if saved_count > 0:
        try:
            session.commit()
            print(f"Success! {saved_count} historical probability records saved to the database.")
        except Exception as e:
            session.rollback()
            print(f"Error saving to database: {e}")
            saved_count = 0
    else:
        print("No new probability records to save.")

    return saved_count

def main():
    # Load environment variables searching from the project root
    load_dotenv(find_dotenv())
    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        print("Error: DATABASE_URL environment variable is not set.")
        print("Create a '.env' file in the monorepo root containing the DATABASE_URL key.")
        sys.exit(1)

    # Standard fix for older PostgreSQL connection strings
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    # Database connection
    print("Initiating connection to PostgreSQL...")
    try:
        engine = create_engine(db_url)
        # Create table if it doesn't exist
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()
    except Exception as e:
        print(f"Database connection failure: {e}")
        sys.exit(1)

    # Run the ETL pipeline
    markets = fetch_markets()
    if markets:
        parse_and_save_markets(markets, session)
    else:
        print("Processing aborted because the API returned no data.")

    session.close()

if __name__ == "__main__":
    main()
