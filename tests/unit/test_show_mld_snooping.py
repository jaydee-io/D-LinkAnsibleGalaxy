"""Unit tests for show_mld_snooping module."""

from show_mld_snooping import _build_command


def test_all():
    assert _build_command(None) == "show ipv6 mld snooping"


def test_vlan():
    assert _build_command(1) == "show ipv6 mld snooping vlan 1"
