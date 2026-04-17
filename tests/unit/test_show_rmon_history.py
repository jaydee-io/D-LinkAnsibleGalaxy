"""Unit tests for show_rmon_history module command builder."""

from show_rmon_history import _build_command


def test_command():
    assert _build_command() == "show rmon history"
