"""Unit tests for show_mld_snooping_static_group module."""

from show_mld_snooping_static_group import _build_command


def test_no_params():
    assert _build_command(None, None) == "show ipv6 mld snooping static-group"


def test_group_address():
    assert _build_command("FF02::1:FF00:1", None) == "show ipv6 mld snooping static-group FF02::1:FF00:1"


def test_vlan():
    assert _build_command(None, 1) == "show ipv6 mld snooping static-group vlan 1"
