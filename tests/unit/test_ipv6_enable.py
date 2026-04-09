"""Unit tests for ipv6_enable module command builder."""

from ipv6_enable import _build_commands


def test_enabled():
    assert _build_commands("vlan1", "enabled") == [
        "interface vlan1",
        "ipv6 enable",
        "exit",
    ]


def test_disabled():
    assert _build_commands("vlan1", "disabled") == [
        "interface vlan1",
        "no ipv6 enable",
        "exit",
    ]
