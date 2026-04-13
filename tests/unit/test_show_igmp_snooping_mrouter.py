"""Unit tests for show_igmp_snooping_mrouter module."""

from show_igmp_snooping_mrouter import _build_command


def test_no_params():
    assert _build_command(None) == "show ip igmp snooping mrouter"


def test_vlan():
    assert _build_command(1) == "show ip igmp snooping mrouter vlan 1"
