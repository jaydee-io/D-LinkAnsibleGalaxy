"""Unit tests for igmp_snooping_minimum_version module."""

from igmp_snooping_minimum_version import _build_commands


def test_present_v2():
    assert _build_commands(1, 2, "present") == [
        "vlan 1",
        "ip igmp snooping minimum-version 2",
        "exit",
    ]


def test_present_v3():
    assert _build_commands(1, 3, "present") == [
        "vlan 1",
        "ip igmp snooping minimum-version 3",
        "exit",
    ]


def test_absent():
    assert _build_commands(1, None, "absent") == [
        "vlan 1",
        "no ip igmp snooping minimum-version",
        "exit",
    ]
