"""Unit tests for show_igmp_snooping_statistics module."""

from show_igmp_snooping_statistics import _build_command


def test_interface_all():
    assert _build_command("interface", None, None) == "show ip igmp snooping statistics interface"


def test_interface_specific():
    assert _build_command("interface", "eth1/0/1", None) == (
        "show ip igmp snooping statistics interface eth1/0/1"
    )


def test_vlan_all():
    assert _build_command("vlan", None, None) == "show ip igmp snooping statistics vlan"


def test_vlan_specific():
    assert _build_command("vlan", None, 1) == "show ip igmp snooping statistics vlan 1"
