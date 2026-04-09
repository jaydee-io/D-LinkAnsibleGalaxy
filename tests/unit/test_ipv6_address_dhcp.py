"""Unit tests for ipv6_address_dhcp module command builder."""

from ipv6_address_dhcp import _build_commands


def test_present():
    assert _build_commands("vlan1", False, "present") == [
        "interface vlan1",
        "ipv6 address dhcp",
        "exit",
    ]


def test_present_rapid_commit():
    assert _build_commands("vlan1", True, "present") == [
        "interface vlan1",
        "ipv6 address dhcp rapid-commit",
        "exit",
    ]


def test_absent():
    assert _build_commands("vlan1", False, "absent") == [
        "interface vlan1",
        "no ipv6 address dhcp",
        "exit",
    ]
