"""Unit tests for igmp_snooping_query_max_response_time module."""

from igmp_snooping_query_max_response_time import _build_commands


def test_present():
    assert _build_commands(1000, 20, "present") == [
        "vlan 1000",
        "ip igmp snooping query-max-response-time 20",
        "exit",
    ]


def test_absent():
    assert _build_commands(1000, None, "absent") == [
        "vlan 1000",
        "no ip igmp snooping query-max-response-time",
        "exit",
    ]
