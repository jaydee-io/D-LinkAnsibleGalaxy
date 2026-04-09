"""Unit tests for ipv6_nd_suppress_ra module command builder."""

from ipv6_nd_suppress_ra import _build_commands


def test_enabled():
    assert _build_commands("vlan1", "enabled") == [
        "interface vlan1",
        "ipv6 nd suppress-ra",
        "exit",
    ]


def test_disabled():
    assert _build_commands("vlan1", "disabled") == [
        "interface vlan1",
        "no ipv6 nd suppress-ra",
        "exit",
    ]
