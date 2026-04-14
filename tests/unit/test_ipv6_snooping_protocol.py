"""Unit tests for ipv6_snooping_protocol module."""

from ipv6_snooping_protocol import _build_commands


def test_present_dhcp():
    assert _build_commands("policy1", "dhcp", "present") == [
        "ipv6 snooping policy policy1",
        "protocol dhcp",
        "exit",
    ]


def test_present_ndp():
    assert _build_commands("policy1", "ndp", "present") == [
        "ipv6 snooping policy policy1",
        "protocol ndp",
        "exit",
    ]


def test_absent():
    assert _build_commands("policy1", "dhcp", "absent") == [
        "ipv6 snooping policy policy1",
        "no protocol dhcp",
        "exit",
    ]
