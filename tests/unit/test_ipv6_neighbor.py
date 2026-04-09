"""Unit tests for ipv6_neighbor module command builder."""

from ipv6_neighbor import _build_commands


def test_present():
    assert _build_commands("2001:db8::1", "vlan1", "00-01-02-03-04-05", "present") == [
        "ipv6 neighbor 2001:db8::1 vlan1 00-01-02-03-04-05",
    ]


def test_absent():
    assert _build_commands("2001:db8::1", "vlan1", None, "absent") == [
        "no ipv6 neighbor 2001:db8::1 vlan1",
    ]
