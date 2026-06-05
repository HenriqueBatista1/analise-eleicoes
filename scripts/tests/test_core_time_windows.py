from core.time_windows import calculate_incremental_start_timestamp
from tests.helpers import naive_utc_datetime, utc_timestamp


def test_calculate_incremental_start_timestamp_returns_none_without_previous_timestamp():
    assert calculate_incremental_start_timestamp(None) is None


def test_calculate_incremental_start_timestamp_applies_one_day_overlap():
    last_timestamp = naive_utc_datetime(2024, 1, 2)

    start_ts = calculate_incremental_start_timestamp(last_timestamp)

    assert start_ts == utc_timestamp(2024, 1, 1)


def test_calculate_incremental_start_timestamp_never_returns_negative_timestamp():
    last_timestamp = naive_utc_datetime(1970, 1, 1, 1)

    start_ts = calculate_incremental_start_timestamp(last_timestamp)

    assert start_ts == 0
