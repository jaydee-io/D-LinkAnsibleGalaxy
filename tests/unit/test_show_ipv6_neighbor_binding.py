"""Unit tests for show_ipv6_neighbor_binding module."""

from show_ipv6_neighbor_binding import _build_command


def test_no_params():
    assert _build_command(None, None, None, None) == "show ipv6 neighbor binding"


def test_vlan():
    assert _build_command(100, None, None, None) == "show ipv6 neighbor binding vlan 100"


def test_interface():
    assert _build_command(None, "eth1/0/1", None, None) == (
        "show ipv6 neighbor binding interface eth1/0/1"
    )


def test_ipv6():
    assert _build_command(None, None, "2001::1", None) == (
        "show ipv6 neighbor binding ipv6 2001::1"
    )


def test_mac():
    assert _build_command(None, None, None, "AABB.CC01.F500") == (
        "show ipv6 neighbor binding mac AABB.CC01.F500"
    )


def test_all_params():
    assert _build_command(100, "eth1/0/1", "2001::1", "AABB.CC01.F500") == (
        "show ipv6 neighbor binding vlan 100 interface eth1/0/1 ipv6 2001::1 mac AABB.CC01.F500"
    )
