"""Unit tests for monitor_session_destination module."""

from monitor_session_destination import _build_commands


def test_set():
    assert _build_commands(1, "eth1/0/1", "present") == [
        "monitor session 1 destination interface eth1/0/1"]


def test_remove():
    assert _build_commands(1, None, "absent") == ["no monitor session 1"]
