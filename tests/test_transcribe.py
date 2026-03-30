import pytest
from transcribe import format_timestamp


@pytest.mark.parametrize("seconds, expected", [
    (0,     "0:00"),
    (59,    "0:59"),
    (60,    "1:00"),
    (90,    "1:30"),
    (3599,  "59:59"),
    (3600,  "1:00:00"),
    (3661,  "1:01:01"),
    (7322,  "2:02:02"),
])
def test_format_timestamp(seconds, expected):
    assert format_timestamp(seconds) == expected
