"""Unit tests for show_lldp_management_address module."""

from show_lldp_management_address import _build_command


def test_all():
    assert _build_command(None) == "show lldp management-address"


def test_specific():
    assert _build_command("10.90.90.90") == "show lldp management-address 10.90.90.90"
