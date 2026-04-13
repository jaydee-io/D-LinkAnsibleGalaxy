"""Unit tests for igmp_snooping_mrouter module."""

from igmp_snooping_mrouter import _build_commands


def test_add_interface():
    assert _build_commands(1, "interface", "eth1/0/4", "present") == [
        "vlan 1",
        "ip igmp snooping mrouter interface eth1/0/4",
        "exit",
    ]


def test_remove_interface():
    assert _build_commands(1, "interface", "eth1/0/4", "absent") == [
        "vlan 1",
        "no ip igmp snooping mrouter interface eth1/0/4",
        "exit",
    ]


def test_add_forbidden():
    assert _build_commands(1, "forbidden", "eth1/0/5", "present") == [
        "vlan 1",
        "ip igmp snooping mrouter forbidden interface eth1/0/5",
        "exit",
    ]


def test_remove_forbidden():
    assert _build_commands(1, "forbidden", "eth1/0/5", "absent") == [
        "vlan 1",
        "no ip igmp snooping mrouter forbidden interface eth1/0/5",
        "exit",
    ]
