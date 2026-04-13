"""Unit tests for show_igmp_snooping_groups module."""

from show_igmp_snooping_groups import _build_command


def test_no_params():
    assert _build_command(None, None) == "show ip igmp snooping groups"


def test_vlan():
    assert _build_command(1, None) == "show ip igmp snooping groups vlan 1"


def test_ip_address():
    assert _build_command(None, "239.255.255.250") == "show ip igmp snooping groups 239.255.255.250"
