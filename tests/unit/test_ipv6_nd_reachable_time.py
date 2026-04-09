"""Unit tests for ipv6_nd_reachable_time module command builder."""

from ipv6_nd_reachable_time import _build_commands


def test_present():
    assert _build_commands("vlan1", 30000, "present") == [
        "interface vlan1",
        "ipv6 nd reachable-time 30000",
        "exit",
    ]


def test_absent():
    assert _build_commands("vlan1", None, "absent") == [
        "interface vlan1",
        "no ipv6 nd reachable-time",
        "exit",
    ]
