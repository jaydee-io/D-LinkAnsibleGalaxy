"""Unit tests for show_rmon_statistics module command builder."""

from show_rmon_statistics import _build_command


def test_command():
    assert _build_command() == "show rmon statistics"
