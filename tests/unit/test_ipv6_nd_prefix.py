"""Unit tests for ipv6_nd_prefix module command builder."""

from ipv6_nd_prefix import _build_commands


def test_present_basic():
    assert _build_commands("vlan1", "2001:db8::", 64, None, None, False, False, "present") == [
        "interface vlan1",
        "ipv6 nd prefix 2001:db8::/64",
        "exit",
    ]


def test_present_with_lifetimes():
    assert _build_commands("vlan1", "2001:db8::", 64, 2592000, 604800, False, False, "present") == [
        "interface vlan1",
        "ipv6 nd prefix 2001:db8::/64 2592000 604800",
        "exit",
    ]


def test_present_with_off_link():
    assert _build_commands("vlan1", "2001:db8::", 64, None, None, True, False, "present") == [
        "interface vlan1",
        "ipv6 nd prefix 2001:db8::/64 off-link",
        "exit",
    ]


def test_present_with_no_autoconfig():
    assert _build_commands("vlan1", "2001:db8::", 64, None, None, False, True, "present") == [
        "interface vlan1",
        "ipv6 nd prefix 2001:db8::/64 no-autoconfig",
        "exit",
    ]


def test_present_all_options():
    assert _build_commands("vlan1", "2001:db8::", 64, 2592000, 604800, True, True, "present") == [
        "interface vlan1",
        "ipv6 nd prefix 2001:db8::/64 2592000 604800 off-link no-autoconfig",
        "exit",
    ]


def test_absent():
    assert _build_commands("vlan1", "2001:db8::", 64, None, None, False, False, "absent") == [
        "interface vlan1",
        "no ipv6 nd prefix 2001:db8::/64",
        "exit",
    ]
