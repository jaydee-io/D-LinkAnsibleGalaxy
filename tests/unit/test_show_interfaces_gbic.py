"""Unit tests for show_interfaces_gbic module."""

from show_interfaces_gbic import _build_command


def test_all():
    assert _build_command(None) == "show interfaces gbic"


def test_specific():
    assert _build_command("eth1/0/1-8") == "show interfaces eth1/0/1-8 gbic"
