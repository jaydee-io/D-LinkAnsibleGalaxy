"""Unit tests for show_rmon_events module command builder."""

from show_rmon_events import _build_command


def test_command():
    assert _build_command() == "show rmon events"
