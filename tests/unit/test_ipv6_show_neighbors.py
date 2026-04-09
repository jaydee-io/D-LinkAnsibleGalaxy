"""Unit tests for ipv6_show_neighbors module parser."""

from ipv6_show_neighbors import _parse_neighbors


def test_parse_entries():
    output = """\
IPv6 Address              Link-Layer Addr   Interface  Type     State
------------------------  ----------------  ---------  -------  -----
2001:db8::1               00-01-02-03-04-05 vlan1      Static   REACH
fe80::1                   00-0a-0b-0c-0d-0e vlan1      Dynamic  STALE

Total Entries: 2
"""
    entries, total = _parse_neighbors(output)
    assert len(entries) == 2
    assert entries[0]["ipv6_address"] == "2001:db8::1"
    assert entries[0]["link_layer_addr"] == "00-01-02-03-04-05"
    assert entries[0]["interface"] == "vlan1"
    assert entries[0]["type"] == "Static"
    assert entries[0]["state"] == "REACH"
    assert entries[1]["ipv6_address"] == "fe80::1"
    assert entries[1]["link_layer_addr"] == "00-0a-0b-0c-0d-0e"
    assert entries[1]["interface"] == "vlan1"
    assert entries[1]["type"] == "Dynamic"
    assert entries[1]["state"] == "STALE"
    assert total == 2


def test_empty():
    output = """\
IPv6 Address              Link-Layer Addr   Interface  Type     State
------------------------  ----------------  ---------  -------  -----

Total Entries: 0
"""
    entries, total = _parse_neighbors(output)
    assert entries == []
    assert total == 0
