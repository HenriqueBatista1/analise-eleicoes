from constants import (
    POLYMARKET_GAMMA_EVENT_URL,
    POLYMARKET_HISTORY_FIDELITY_MINUTES,
    POLYMARKET_PRICE_HISTORY_URL,
)
from extractors import polymarket
from tests.helpers import utc_timestamp


class ApiResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


def test_fetch_event_markets_requests_configured_event(monkeypatch):
    request_calls = []
    event_id = "event-123"
    expected_markets = [{"id": "market-1"}]

    def fake_get(url, timeout):
        request_calls.append({"url": url, "timeout": timeout})
        return ApiResponse({"markets": expected_markets})

    monkeypatch.setattr(polymarket.requests, "get", fake_get)

    markets = polymarket.fetch_event_markets(event_id)

    assert markets == expected_markets
    assert request_calls == [
        {
            "url": POLYMARKET_GAMMA_EVENT_URL.format(event_id=event_id),
            "timeout": 30,
        }
    ]


def test_fetch_price_history_uses_max_interval_for_initial_load(monkeypatch):
    request_calls = []

    def fake_get(url, params, timeout):
        request_calls.append({"url": url, "params": params, "timeout": timeout})
        return ApiResponse({"history": []})

    monkeypatch.setattr(polymarket.requests, "get", fake_get)

    history = polymarket.fetch_price_history(token_id="yes-token")

    assert history == []
    assert request_calls == [
        {
            "url": POLYMARKET_PRICE_HISTORY_URL,
            "params": {
                "market": "yes-token",
                "fidelity": POLYMARKET_HISTORY_FIDELITY_MINUTES,
                "interval": "max",
            },
            "timeout": 30,
        }
    ]


def test_fetch_price_history_uses_time_window_for_incremental_load(monkeypatch):
    request_calls = []
    start_ts = utc_timestamp(2024, 1, 1)
    end_ts = utc_timestamp(2024, 1, 1, 1)
    expected_history = [{"t": start_ts, "p": 0.42}]

    def fake_get(url, params, timeout):
        request_calls.append({"url": url, "params": params, "timeout": timeout})
        return ApiResponse({"history": expected_history})

    monkeypatch.setattr(polymarket.requests, "get", fake_get)

    history = polymarket.fetch_price_history(
        token_id="yes-token",
        start_ts=start_ts,
        end_ts=end_ts,
    )

    assert history == expected_history
    assert request_calls == [
        {
            "url": POLYMARKET_PRICE_HISTORY_URL,
            "params": {
                "market": "yes-token",
                "fidelity": POLYMARKET_HISTORY_FIDELITY_MINUTES,
                "startTs": start_ts,
                "endTs": end_ts,
            },
            "timeout": 30,
        }
    ]
