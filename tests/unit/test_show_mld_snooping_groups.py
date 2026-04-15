"""Unit tests for show_mld_snooping_groups module."""

from show_mld_snooping_groups import _build_command


def test_all():
    assert _build_command(None, None) == "show ipv6 mld snooping groups"


def test_vlan():
    assert _build_command(None, 1) == "show ipv6 mld snooping groups vlan 1"


def test_group():
    assert _build_command("FF1E::", None) == "show ipv6 mld snooping groups FF1E::"
