"""Unit tests for ipv4_arp_timeout module command builder."""

from ipv4_arp_timeout import _build_commands


def test_present():
    assert _build_commands("vlan1", 60, "present") == [
        "interface vlan1",
        "arp timeout 60",
        "exit",
    ]


def test_absent():
    assert _build_commands("vlan1", None, "absent") == [
        "interface vlan1",
        "no arp timeout",
        "exit",
    ]
