"""Unit tests for igmp_snooping_clear_statistics module."""

from igmp_snooping_clear_statistics import _build_commands


def test_clear_all():
    assert _build_commands("all", None, None) == ["clear ip igmp snooping statistics all"]


def test_clear_vlan():
    assert _build_commands("vlan", 10, None) == ["clear ip igmp snooping statistics vlan 10"]


def test_clear_interface():
    assert _build_commands("interface", None, "eth1/0/1") == [
        "clear ip igmp snooping statistics interface eth1/0/1"
    ]
