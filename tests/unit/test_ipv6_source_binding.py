"""Unit tests for ipv6_source_binding module."""

from ipv6_source_binding import _build_commands


def test_present():
    assert _build_commands("00-01-02-03-04-05", 2, "2000::1", "eth1/0/1", "present") == [
        "ipv6 source binding 00-01-02-03-04-05 vlan 2 2000::1 interface eth1/0/1"
    ]


def test_absent():
    assert _build_commands("00-01-02-03-04-05", 2, "2000::1", "eth1/0/1", "absent") == [
        "no ipv6 source binding 00-01-02-03-04-05 vlan 2 2000::1 interface eth1/0/1"
    ]
