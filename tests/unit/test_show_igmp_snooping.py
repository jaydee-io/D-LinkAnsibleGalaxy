"""Unit tests for show_igmp_snooping module."""

from show_igmp_snooping import _build_command


def test_no_params():
    assert _build_command(None) == "show ip igmp snooping"


def test_vlan():
    assert _build_command(2) == "show ip igmp snooping vlan 2"
