# Backend

This document defines stable backend architecture decisions for the project.

Product and domain module definitions are documented in `docs/modules.md`.

Database schema and persistence decisions are documented in `docs/database.md`.

## Stack

The backend uses:

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- python-dotenv
- pytest

## Application model

The backend is an HTTP API that serves processed analytical data to the frontend.

The backend reads persisted analytical data and exposes stable frontend-facing contracts.

Route paths are organized by product area and exposed under the `/api` prefix.

FastAPI provides interactive API documentation at `/docs` during development.

The generated documentation is useful for manual endpoint inspection and request testing, but stable architecture and product decisions remain documented in the repository.

## Project structure

```text
backend/
  app/
    core/
    routers/
    schemas/
    services/
    main.py
    models.py
  tests/
```

Core configuration and database session helpers stay in `app/core`.

Route declarations stay in `app/routers`. `app/routers/api.py` owns the global `/api` prefix.

Response schemas stay in `app/schemas`.

Database read logic and response assembly stay in `app/services`.

## API contracts

### Current Election: Market Expectations

```text
GET /api/current-election/market-expectations
```

Returns market expectation data for the current election using Polymarket as the current source.

Supported query parameters:

- `fromDate`: optional ISO datetime lower bound for returned series points.
- `toDate`: optional ISO datetime upper bound for returned series points.
- `interval`: optional series interval. Supported values are `1h`, `4h`, `1d` and `1w`. Default is `1h`.
- `candidateCatalogIds`: optional array of candidate catalog identifiers. In query strings, send multiple values by repeating the parameter, for example `?candidateCatalogIds=1&candidateCatalogIds=2`.

Date filters are inclusive. If the selected range has no matching records, the endpoint returns an empty `series` list.

Unknown candidate catalog identifiers do not produce an error. They return an empty `series` list when no records match.

The response includes:

- `sources`: data sources used by the endpoint.
- `metadata.latestTimestamp`: latest available Polymarket timestamp in the database.
- `summary.currentLeader`: candidate with the highest latest probability in the returned series.
- `summary.leaderMargin`: difference between the leader and runner-up latest probabilities in the returned series.
- `summary.largestChange`: largest absolute probability variation in the returned series, preserving the signed variation.
- `series`: time series grouped by candidate catalog entry and market.

Probability values are returned in their stored analytical range from `0.0` to `1.0`.

For aggregated intervals, the backend returns the latest real record inside each time bucket. It does not create synthetic points or interpolate missing data.

## Configuration

The backend reads `DATABASE_URL` from the project environment.

## Testing

Run backend unit tests from inside `/backend`.

Use `python -m pytest tests`.
