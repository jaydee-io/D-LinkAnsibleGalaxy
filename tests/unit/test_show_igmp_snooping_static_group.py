"""Unit tests for show_igmp_snooping_static_group module."""

from show_igmp_snooping_static_group import _build_command


def test_no_params():
    assert _build_command(None, None) == "show ip igmp snooping static-group"


def test_group_address():
    assert _build_command("226.1.2.2", None) == "show ip igmp snooping static-group 226.1.2.2"


def test_vlan():
    assert _build_command(None, 1) == "show ip igmp snooping static-group vlan 1"
