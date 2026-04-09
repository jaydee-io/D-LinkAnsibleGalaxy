"""Unit tests for ipv4_show_arp module parser."""

from ipv4_show_arp import _parse_arp


def test_parse_entries():
    output = """\
S - Static Entry

IP Address        Hardware Addr     IP Interface  Age (min)
----------------  ----------------  ------------  ---------------
S 10.31.7.19      08-00-09-00-18-34 vlan1         forever
  10.90.90.90     00-01-02-03-04-00 vlan1         forever

Total Entries: 2
"""
    entries, total = _parse_arp(output)
    assert len(entries) == 2
    assert entries[0]["static"] is True
    assert entries[0]["ip_address"] == "10.31.7.19"
    assert entries[0]["hardware_address"] == "08-00-09-00-18-34"
    assert entries[0]["interface"] == "vlan1"
    assert entries[0]["age"] == "forever"
    assert entries[1]["static"] is False
    assert entries[1]["ip_address"] == "10.90.90.90"
    assert entries[1]["hardware_address"] == "00-01-02-03-04-00"
    assert total == 2


def test_empty():
    output = """\
S - Static Entry

IP Address        Hardware Addr     IP Interface  Age (min)
----------------  ----------------  ------------  ---------------

Total Entries: 0
"""
    entries, total = _parse_arp(output)
    assert entries == []
    assert total == 0
