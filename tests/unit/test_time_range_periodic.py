"""Unit tests for time_range_periodic module."""

from time_range_periodic import _build_commands


def test_add_daily():
    assert _build_commands("rdtime", "daily", "9:00", "12:00", "present") == [
        "time-range rdtime", "periodic daily 9:00 to 12:00", "exit"]


def test_add_weekly():
    assert _build_commands("rdtime", "weekly", "saturday 00:00", "monday 00:00", "present") == [
        "time-range rdtime", "periodic weekly saturday 00:00 to monday 00:00", "exit"]


def test_remove_daily():
    assert _build_commands("rdtime", "daily", "9:00", "12:00", "absent") == [
        "time-range rdtime", "no periodic daily 9:00 to 12:00", "exit"]
