"""Unit tests for clear_counters module."""

from clear_counters import _build_commands


def test_clear_all():
    assert _build_commands("all", None) == ["clear counters all"]


def test_clear_interface():
    assert _build_commands("interface", "eth1/0/1") == ["clear counters interface eth1/0/1"]
