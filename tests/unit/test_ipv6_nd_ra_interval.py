"""Unit tests for ipv6_nd_ra_interval module command builder."""

from ipv6_nd_ra_interval import _build_commands


def test_present_max_only():
    assert _build_commands("vlan1", 600, None, "present") == [
        "interface vlan1",
        "ipv6 nd ra interval 600",
        "exit",
    ]


def test_present_max_and_min():
    assert _build_commands("vlan1", 600, 200, "present") == [
        "interface vlan1",
        "ipv6 nd ra interval 600 200",
        "exit",
    ]


def test_absent():
    assert _build_commands("vlan1", None, None, "absent") == [
        "interface vlan1",
        "no ipv6 nd ra interval",
        "exit",
    ]
