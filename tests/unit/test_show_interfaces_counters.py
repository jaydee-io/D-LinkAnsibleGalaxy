"""Unit tests for show_interfaces_counters module."""

from show_interfaces_counters import _build_command


def test_all():
    assert _build_command(None, False) == "show interfaces counters"


def test_specific():
    assert _build_command("eth1/0/1-8", False) == "show interfaces eth1/0/1-8 counters"


def test_errors():
    assert _build_command("eth1/0/1-8", True) == "show interfaces eth1/0/1-8 counters errors"
