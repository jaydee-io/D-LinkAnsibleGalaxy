"""Unit tests for igmp_snooping_query_interval module."""

from igmp_snooping_query_interval import _build_commands


def test_present():
    assert _build_commands(1000, 300, "present") == [
        "vlan 1000",
        "ip igmp snooping query-interval 300",
        "exit",
    ]


def test_absent():
    assert _build_commands(1000, None, "absent") == [
        "vlan 1000",
        "no ip igmp snooping query-interval",
        "exit",
    ]
