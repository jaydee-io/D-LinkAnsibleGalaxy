"""Unit tests for ipv6_address module command builder."""

from ipv6_address import _build_commands


def test_present_with_prefix():
    assert _build_commands("vlan1", "2001:db8::1", 64, False, "present") == [
        "interface vlan1",
        "ipv6 address 2001:db8::1/64",
        "exit",
    ]


def test_present_link_local():
    assert _build_commands("vlan1", "fe80::1", None, True, "present") == [
        "interface vlan1",
        "ipv6 address fe80::1 link-local",
        "exit",
    ]


def test_absent_with_prefix():
    assert _build_commands("vlan1", "2001:db8::1", 64, False, "absent") == [
        "interface vlan1",
        "no ipv6 address 2001:db8::1/64",
        "exit",
    ]


def test_absent_link_local():
    assert _build_commands("vlan1", "fe80::1", None, True, "absent") == [
        "interface vlan1",
        "no ipv6 address fe80::1 link-local",
        "exit",
    ]
