"""Unit tests for ipv6_nd_ra_lifetime module command builder."""

from ipv6_nd_ra_lifetime import _build_commands


def test_present():
    assert _build_commands("vlan1", 1800, "present") == [
        "interface vlan1",
        "ipv6 nd ra lifetime 1800",
        "exit",
    ]


def test_absent():
    assert _build_commands("vlan1", None, "absent") == [
        "interface vlan1",
        "no ipv6 nd ra lifetime",
        "exit",
    ]
