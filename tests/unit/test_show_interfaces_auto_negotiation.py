"""Unit tests for show_interfaces_auto_negotiation module."""

from show_interfaces_auto_negotiation import _build_command


def test_all():
    assert _build_command(None) == "show interfaces auto-negotiation"


def test_specific():
    assert _build_command("eth1/0/1-2") == "show interfaces eth1/0/1-2 auto-negotiation"
