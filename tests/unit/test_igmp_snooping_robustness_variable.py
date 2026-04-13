"""Unit tests for igmp_snooping_robustness_variable module."""

from igmp_snooping_robustness_variable import _build_commands


def test_present():
    assert _build_commands(1000, 3, "present") == [
        "vlan 1000",
        "ip igmp snooping robustness-variable 3",
        "exit",
    ]


def test_absent():
    assert _build_commands(1000, None, "absent") == [
        "vlan 1000",
        "no ip igmp snooping robustness-variable",
        "exit",
    ]
