import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from models import Base
from transformers.polymarket import PolymarketMarket


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def market_payload():
    return {
        "id": "market-1",
        "groupItemTitle": "Candidate A",
        "clobTokenIds": '["yes-token", "no-token"]',
    }


@pytest.fixture
def candidate_market():
    return PolymarketMarket(
        market_id="market-1",
        candidate_name="Candidate A",
        yes_token_id="yes-token",
    )
