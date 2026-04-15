"""Unit tests for monitor_session_source module."""

from monitor_session_source import _build_commands


def test_add_default():
    assert _build_commands(1, "eth1/0/2-4", None, "present") == [
        "monitor session 1 source interface eth1/0/2-4"]


def test_add_rx():
    assert _build_commands(1, "eth1/0/5", "rx", "present") == [
        "monitor session 1 source interface eth1/0/5 rx"]


def test_remove():
    assert _build_commands(1, "eth1/0/5", None, "absent") == [
        "no monitor session 1 source interface eth1/0/5"]
