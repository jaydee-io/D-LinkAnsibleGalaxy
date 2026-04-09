"""Unit tests for ipv6_clear_neighbors module command builder."""

from ipv6_clear_neighbors import _build_commands


def test_clear_all():
    assert _build_commands("all", None) == [
        "clear ipv6 neighbors all",
    ]


def test_clear_interface():
    assert _build_commands("interface", "vlan1") == [
        "clear ipv6 neighbors interface vlan1",
    ]
