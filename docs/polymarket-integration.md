# Polymarket API Integration

This document explains the configuration, endpoints, and logic used to fetch election data from Polymarket.

---

## 1. Target Event

- **Event ID**: `45915`
- **Slug**: `brazil-presidential-election`
- **Gamma API Event Endpoint**: `https://gamma-api.polymarket.com/events/45915`
  - Returns metadata for the event and a list of associated `markets`.

---

## 2. Market & Candidate Selection

- **Candidate Names**: Extracted from the `groupItemTitle` field of each market in the event payload (e.g., "Luiz Inácio Lula da Silva", "Michelle Bolsonaro").
- **Filtering Placeholder Markets**: Any market with a candidate name containing `"person "` or `"another person"` (case-insensitive) is skipped as it represents placeholder slots.
- **Token Resolution**:
  - Each binary market contains a `clobTokenIds` list (represented as a JSON-encoded string or array).
  - The **first token ID (index `0`)** corresponds to the `"Yes"` outcome (victory probability).

---

## 3. Historical Price Extraction

- **CLOB History Endpoint**: `https://clob.polymarket.com/prices-history`
- **Query Parameters**:
  - `market`: The `"Yes"` token ID (resolved from `clobTokenIds[0]`).
  - `interval`: `"max"` (gets the full daily historical series from the token's creation date).
- **Response Format**:
  - The API returns a list of data point dictionaries:
    ```json
    [
      {
        "t": 1777795203,
        "p": 0.0015
      },
      ...
    ]
    ```
  - `t`: Unix epoch timestamp in seconds.
  - `p`: Probability of the candidate winning (normalized between `0.0` and `1.0`).

---

## 4. Ingestion & Execution Strategy

- **Update Frequency**: Polymarket data changes rapidly. The pipeline is designed to be executed on a scheduled trigger **daily** or **every 4 hours** to capture fresh snapshots.
- **Incremental Runs**: The ETL script supports incremental runs. Since it queries existing database timestamps, re-running the script will only append the latest daily snapshots generated since the last execution.
