"""Unit tests for ipv4_ip_address module command builder."""

from ipv4_ip_address import _build_commands


def test_static_ip():
    assert _build_commands("vlan1", "10.90.90.90", "255.0.0.0", False, "present") == [
        "interface vlan1",
        "ip address 10.90.90.90 255.0.0.0",
        "exit",
    ]


def test_dhcp():
    assert _build_commands("vlan1", None, None, True, "present") == [
        "interface vlan1",
        "ip address dhcp",
        "exit",
    ]


def test_absent_static():
    assert _build_commands("vlan1", "10.90.90.90", "255.0.0.0", False, "absent") == [
        "interface vlan1",
        "no ip address 10.90.90.90 255.0.0.0",
        "exit",
    ]


def test_absent_dhcp():
    assert _build_commands("vlan1", None, None, True, "absent") == [
        "interface vlan1",
        "no ip address dhcp",
        "exit",
    ]
