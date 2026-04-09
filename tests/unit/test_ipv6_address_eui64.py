"""Unit tests for ipv6_address_eui64 module command builder."""

from ipv6_address_eui64 import _build_commands


def test_present():
    assert _build_commands("vlan1", "2001:db8::", 64, "present") == [
        "interface vlan1",
        "ipv6 address 2001:db8::/64 eui-64",
        "exit",
    ]


def test_absent():
    assert _build_commands("vlan1", "2001:db8::", 64, "absent") == [
        "interface vlan1",
        "no ipv6 address 2001:db8::/64 eui-64",
        "exit",
    ]
