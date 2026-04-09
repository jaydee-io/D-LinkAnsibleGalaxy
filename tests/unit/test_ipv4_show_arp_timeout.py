"""Unit tests for ipv4_show_arp_timeout module parser."""

from ipv4_show_arp_timeout import _parse_arp_timeout


def test_single_interface():
    output = """\
Interface       ARP Timeout (min)
--------------  -----------------
vlan1           240
"""
    entries = _parse_arp_timeout(output)
    assert len(entries) == 1
    assert entries[0]["interface"] == "vlan1"
    assert entries[0]["timeout"] == 240


def test_multiple_interfaces():
    output = """\
Interface       ARP Timeout (min)
--------------  -----------------
vlan1           240
vlan2           60
"""
    entries = _parse_arp_timeout(output)
    assert len(entries) == 2
    assert entries[0]["interface"] == "vlan1"
    assert entries[0]["timeout"] == 240
    assert entries[1]["interface"] == "vlan2"
    assert entries[1]["timeout"] == 60


def test_empty():
    output = """\
Interface       ARP Timeout (min)
--------------  -----------------
"""
    entries = _parse_arp_timeout(output)
    assert entries == []
