"""Unit tests for ipv6_hop_limit module command builder."""

from ipv6_hop_limit import _build_commands


def test_present():
    assert _build_commands("vlan1", 64, "present") == [
        "interface vlan1",
        "ipv6 hop-limit 64",
        "exit",
    ]


def test_absent():
    assert _build_commands("vlan1", None, "absent") == [
        "interface vlan1",
        "no ipv6 hop-limit",
        "exit",
    ]
