"""Unit tests for ipv4_clear_arp_cache module command builder."""

from ipv4_clear_arp_cache import _build_commands


def test_clear_all():
    assert _build_commands("all", None) == [
        "clear arp-cache all",
    ]


def test_clear_interface():
    assert _build_commands("interface", "vlan1") == [
        "clear arp-cache interface vlan1",
    ]


def test_clear_ip():
    assert _build_commands("ip", "10.0.0.1") == [
        "clear arp-cache 10.0.0.1",
    ]
