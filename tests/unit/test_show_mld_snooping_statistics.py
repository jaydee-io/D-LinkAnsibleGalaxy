"""Unit tests for show_mld_snooping_statistics module."""

from show_mld_snooping_statistics import _build_command


def test_all():
    assert _build_command(None) == "show ipv6 mld snooping statistics"


def test_vlan():
    assert _build_command(1) == "show ipv6 mld snooping statistics vlan 1"
