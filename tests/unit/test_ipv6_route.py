"""Unit tests for ipv6_route module command builder."""

from ipv6_route import _build_commands


def test_add():
    assert _build_commands("2001:0101::/32", "vlan1", "fe80::ff:1111:2233", None, "present") == [
        "ipv6 route 2001:0101::/32 vlan1 fe80::ff:1111:2233",
    ]


def test_add_default():
    assert _build_commands("default", None, "2001::1", None, "present") == [
        "ipv6 route default 2001::1",
    ]


def test_add_primary():
    assert _build_commands("2001:0101::/32", "vlan1", "fe80::1", "primary", "present") == [
        "ipv6 route 2001:0101::/32 vlan1 fe80::1 primary",
    ]


def test_remove():
    assert _build_commands("2001:0101::/32", "vlan1", "fe80::1", None, "absent") == [
        "no ipv6 route 2001:0101::/32 vlan1 fe80::1",
    ]
