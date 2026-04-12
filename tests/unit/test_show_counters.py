"""Unit tests for show_counters module."""

from show_counters import _build_command


def test_all():
    assert _build_command(None) == "show counters"


def test_specific_interface():
    assert _build_command("eth1/0/1") == "show counters interface eth1/0/1"
