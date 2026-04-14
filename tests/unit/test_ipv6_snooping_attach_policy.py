"""Unit tests for ipv6_snooping_attach_policy module."""

from ipv6_snooping_attach_policy import _build_commands


def test_present():
    assert _build_commands(200, "policy1", "present") == [
        "vlan 200",
        "ipv6 snooping policy attach-policy policy1",
        "exit",
    ]


def test_absent():
    assert _build_commands(200, None, "absent") == [
        "vlan 200",
        "no ipv6 snooping policy attach-policy",
        "exit",
    ]
