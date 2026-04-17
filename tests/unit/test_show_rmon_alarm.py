"""Unit tests for show_rmon_alarm module command builder."""

from show_rmon_alarm import _build_command


def test_command():
    assert _build_command() == "show rmon alarm"
