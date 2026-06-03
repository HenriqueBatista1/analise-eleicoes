# Database Schema & Conventions

This document outlines the database schema, models, performance indices, and deduplication logic implemented in the ingestion pipeline.

---

## 1. Current Database Model

The application uses SQLAlchemy to map historical probability snapshots to a PostgreSQL database.

### Table Name: `polymarket_probabilities`

| Column Name      | SQLAlchemy Type               | Nullable | Description                                                           |
| :--------------- | :---------------------------- | :------- | :-------------------------------------------------------------------- |
| `id`             | `Integer` (PK, autoincrement) | No       | Database primary key.                                                 |
| `candidate_name` | `String(100)`                 | No       | Name of the candidate (extracted from `groupItemTitle`).              |
| `probability`    | `Float`                       | No       | Victory probability (from outcome price `'p'`, range: `0.0` - `1.0`). |
| `timestamp`      | `DateTime`                    | No       | UTC timestamp of the snapshot (converted from Unix epoch `'t'`).      |
| `market_id`      | `String(255)`                 | No       | Unique identifier of the specific binary market in Polymarket.        |

### Performance Indexing

To support fast line-chart queries on the frontend, the database schema includes:

- **Composite Index**: `(candidate_name, timestamp)` (named `idx_candidate_timestamp`) to optimize temporal queries filtering by candidate.

---

## 2. In-Memory Deduplication Logic

To prevent writing duplicate records of the same daily price snapshots, `fetch_polymarket.py` implements an optimized in-memory validation step:

1. **Pre-fetch Existing Pairs**: Before iterating over the candidates' histories, the pipeline queries all existing `(market_id, timestamp)` pairs from the database:
   ```python
   existing_records = set(
       session.query(PolymarketProbability.market_id, PolymarketProbability.timestamp).all()
   )
   ```
2. **Batch Checking**: For each daily history point, it constructs `db_timestamp = datetime.utcfromtimestamp(t_sec)` and performs an $O(1)$ set lookup:
   ```python
   if (market_id, db_timestamp) in existing_records:
       continue  # Skip already saved data points
   ```
3. **Session Append & Set Cache Update**: If the point is new, it instantiates the record, adds it to the SQLAlchemy session, and adds the tuple to the `existing_records` set to prevent double-inserting if the API payload contains duplicate items.
4. **Transaction Commit**: Once all candidate histories are parsed, a single transaction commit persists the batch to PostgreSQL.

---

## 3. Future Database Schema Expansion

To support the other data modules outlined in the project blueprint (`AGENTS.md`), future database designs should consider:

### A. Candidate Mapping (Unified Catalog)

To avoid string mismatch issues when merging TSE, Polymarket, Wikipedia, and Google Trends:

- Create a central `candidates` catalog table:
  - `id` (Primary Key)
  - `slug` (Unique identifier, e.g. `luiz-inacio-lula-da-silva`, `jair-bolsonaro`)
  - `display_name` (e.g. "Lula")
  - `tse_name` (Name used in TSE records)
  - `trends_query` (Query term used for Google Trends)
- Update `polymarket_probabilities` and other attention tables to reference this table via a foreign key `candidate_id`.

### B. Mapped Tables for Upcoming Modules

- **`public_attention_snapshots`**:
  - Columns: `candidate_id` (FK), `timestamp` (DateTime), `wikipedia_views` (Integer), `trends_index` (Float).
- **`tse_historical_results`**:
  - Columns: `candidate_id` (FK), `election_year` (Integer), `round` (Integer), `state_code` (String), `votes_count` (Integer).
- **`macroeconomic_indicators`**:
  - Columns: `timestamp` (DateTime), `usd_rate` (Float), `selic_rate` (Float), `ipca_index` (Float), `ibovespa` (Float).
