from datetime import datetime

from tests.helpers import candidate_catalog, polymarket_probability


def test_health_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_market_expectations_returns_empty_series_when_no_data_exists(client):
    response = client.get("/api/current-election/market-expectations")

    assert response.status_code == 200
    assert response.json() == {
        "sources": ["polymarket"],
        "metadata": {
            "latestTimestamp": None,
        },
        "summary": {
            "currentLeader": None,
            "leaderMargin": None,
            "largestChange": None,
        },
        "series": [],
    }


def test_market_expectations_returns_grouped_candidate_series(client, db_session_factory):
    with db_session_factory() as session:
        session.add_all(
            [
                candidate_catalog(
                    candidate_id=1,
                    display_name="Candidate A",
                    source_key="market-1",
                ),
                candidate_catalog(
                    candidate_id=2,
                    display_name="Candidate B",
                    source_key="market-2",
                ),
                polymarket_probability(
                    candidate_catalog_id=1,
                    candidate_name="Candidate A",
                    probability=0.25,
                    timestamp=datetime(2024, 1, 1, 10),
                ),
                polymarket_probability(
                    candidate_catalog_id=1,
                    candidate_name="Candidate A",
                    probability=0.50,
                    timestamp=datetime(2024, 1, 1, 11),
                ),
                polymarket_probability(
                    candidate_catalog_id=2,
                    candidate_name="Candidate B",
                    probability=0.125,
                    timestamp=datetime(2024, 1, 1, 10),
                    market_id="market-2",
                ),
            ]
        )
        session.commit()

    response = client.get("/api/current-election/market-expectations")

    assert response.status_code == 200
    assert response.json() == {
        "sources": ["polymarket"],
        "metadata": {
            "latestTimestamp": "2024-01-01T11:00:00",
        },
        "summary": {
            "currentLeader": {
                "candidateCatalogId": 1,
                "displayName": "Candidate A",
                "probability": 0.5,
            },
            "leaderMargin": {
                "value": 0.375,
                "leaderCandidateCatalogId": 1,
                "runnerUpCandidateCatalogId": 2,
            },
            "largestChange": {
                "candidateCatalogId": 1,
                "displayName": "Candidate A",
                "value": 0.25,
                "absoluteValue": 0.25,
            },
        },
        "series": [
            {
                "candidateCatalogId": 1,
                "candidateName": "Candidate A",
                "displayName": "Candidate A",
                "marketId": "market-1",
                "points": [
                    {
                        "timestamp": "2024-01-01T10:00:00",
                        "probability": 0.25,
                    },
                    {
                        "timestamp": "2024-01-01T11:00:00",
                        "probability": 0.5,
                    },
                ],
            },
            {
                "candidateCatalogId": 2,
                "candidateName": "Candidate B",
                "displayName": "Candidate B",
                "marketId": "market-2",
                "points": [
                    {
                        "timestamp": "2024-01-01T10:00:00",
                        "probability": 0.125,
                    },
                ],
            },
        ],
    }


def test_market_expectations_filters_by_candidate_catalog_ids(client, db_session_factory):
    with db_session_factory() as session:
        session.add_all(
            [
                candidate_catalog(
                    candidate_id=1,
                    display_name="Candidate A",
                    source_key="market-1",
                ),
                candidate_catalog(
                    candidate_id=2,
                    display_name="Candidate B",
                    source_key="market-2",
                ),
                polymarket_probability(
                    candidate_catalog_id=1,
                    candidate_name="Candidate A",
                    probability=0.25,
                    timestamp=datetime(2024, 1, 1, 10),
                ),
                polymarket_probability(
                    candidate_catalog_id=2,
                    candidate_name="Candidate B",
                    probability=0.50,
                    timestamp=datetime(2024, 1, 1, 10),
                    market_id="market-2",
                ),
            ]
        )
        session.commit()

    response = client.get(
        "/api/current-election/market-expectations",
        params={"candidateCatalogIds": 2},
    )

    assert response.status_code == 200
    response_body = response.json()
    assert [series["candidateCatalogId"] for series in response_body["series"]] == [2]
    assert response_body["summary"]["currentLeader"] == {
        "candidateCatalogId": 2,
        "displayName": "Candidate B",
        "probability": 0.5,
    }


def test_market_expectations_returns_empty_series_for_unknown_candidate_catalog_id(
    client,
    db_session_factory,
):
    with db_session_factory() as session:
        session.add_all(
            [
                candidate_catalog(
                    candidate_id=1,
                    display_name="Candidate A",
                    source_key="market-1",
                ),
                polymarket_probability(
                    candidate_catalog_id=1,
                    candidate_name="Candidate A",
                    probability=0.25,
                    timestamp=datetime(2024, 1, 1, 10),
                ),
            ]
        )
        session.commit()

    response = client.get(
        "/api/current-election/market-expectations",
        params={"candidateCatalogIds": 999},
    )

    assert response.status_code == 200
    response_body = response.json()
    assert response_body["metadata"]["latestTimestamp"] == "2024-01-01T10:00:00"
    assert response_body["summary"] == {
        "currentLeader": None,
        "leaderMargin": None,
        "largestChange": None,
    }
    assert response_body["series"] == []


def test_market_expectations_filters_by_date_range(client, db_session_factory):
    with db_session_factory() as session:
        session.add_all(
            [
                candidate_catalog(
                    candidate_id=1,
                    display_name="Candidate A",
                    source_key="market-1",
                ),
                polymarket_probability(
                    candidate_catalog_id=1,
                    candidate_name="Candidate A",
                    probability=0.20,
                    timestamp=datetime(2024, 1, 1, 9),
                ),
                polymarket_probability(
                    candidate_catalog_id=1,
                    candidate_name="Candidate A",
                    probability=0.30,
                    timestamp=datetime(2024, 1, 1, 10),
                ),
                polymarket_probability(
                    candidate_catalog_id=1,
                    candidate_name="Candidate A",
                    probability=0.40,
                    timestamp=datetime(2024, 1, 1, 11),
                ),
            ]
        )
        session.commit()

    response = client.get(
        "/api/current-election/market-expectations",
        params={
            "fromDate": "2024-01-01T10:00:00",
            "toDate": "2024-01-01T10:00:00",
        },
    )

    assert response.status_code == 200
    response_body = response.json()
    assert response_body["metadata"]["latestTimestamp"] == "2024-01-01T11:00:00"
    assert response_body["series"][0]["points"] == [
        {
            "timestamp": "2024-01-01T10:00:00",
            "probability": 0.3,
        }
    ]


def test_market_expectations_returns_empty_series_for_out_of_range_dates(
    client,
    db_session_factory,
):
    with db_session_factory() as session:
        session.add_all(
            [
                candidate_catalog(
                    candidate_id=1,
                    display_name="Candidate A",
                    source_key="market-1",
                ),
                polymarket_probability(
                    candidate_catalog_id=1,
                    candidate_name="Candidate A",
                    probability=0.20,
                    timestamp=datetime(2024, 1, 1, 9),
                ),
            ]
        )
        session.commit()

    response = client.get(
        "/api/current-election/market-expectations",
        params={
            "fromDate": "2024-01-02T00:00:00",
            "toDate": "2024-01-02T23:59:59",
        },
    )

    assert response.status_code == 200
    response_body = response.json()
    assert response_body["metadata"]["latestTimestamp"] == "2024-01-01T09:00:00"
    assert response_body["summary"] == {
        "currentLeader": None,
        "leaderMargin": None,
        "largestChange": None,
    }
    assert response_body["series"] == []


def test_market_expectations_rejects_inverted_date_range(client):
    response = client.get(
        "/api/current-election/market-expectations",
        params={
            "fromDate": "2024-01-02T00:00:00",
            "toDate": "2024-01-01T00:00:00",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "fromDate must be earlier than or equal to toDate.",
    }


def test_market_expectations_rejects_unsupported_interval(client):
    response = client.get(
        "/api/current-election/market-expectations",
        params={"interval": "2h"},
    )

    assert response.status_code == 422
    response_body = response.json()
    assert response_body["detail"][0]["msg"] == "Input should be '1h', '4h', '1d' or '1w'"
    assert response_body["detail"][0]["input"] == "2h"
