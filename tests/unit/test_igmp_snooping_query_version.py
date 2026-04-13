"""Unit tests for igmp_snooping_query_version module."""

from igmp_snooping_query_version import _build_commands


def test_present():
    assert _build_commands(1000, 2, "present") == [
        "vlan 1000",
        "ip igmp snooping query-version 2",
        "exit",
    ]


def test_absent():
    assert _build_commands(1000, None, "absent") == [
        "vlan 1000",
        "no ip igmp snooping query-version",
        "exit",
    ]
