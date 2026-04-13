"""Unit tests for igmp_snooping_static_group module."""

from igmp_snooping_static_group import _build_commands


def test_present():
    assert _build_commands(1, "226.1.2.3", "eth1/0/5", "present") == [
        "vlan 1",
        "ip igmp snooping static-group 226.1.2.3 interface eth1/0/5",
        "exit",
    ]


def test_absent():
    assert _build_commands(1, "226.1.2.3", None, "absent") == [
        "vlan 1",
        "no ip igmp snooping static-group 226.1.2.3",
        "exit",
    ]
