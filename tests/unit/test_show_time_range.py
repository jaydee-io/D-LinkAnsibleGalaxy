"""Unit tests for show_time_range module."""

from show_time_range import _build_command


def test_all():
    assert _build_command(None) == "show time-range"


def test_named():
    assert _build_command("rdtime") == "show time-range rdtime"
