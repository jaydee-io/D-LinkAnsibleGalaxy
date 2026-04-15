"""Unit tests for show_monitor_session module."""

from show_monitor_session import _build_command


def test_all():
    assert _build_command(None) == "show monitor session"


def test_specific():
    assert _build_command(1) == "show monitor session 1"
