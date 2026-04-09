"""Unit tests for ipv4_show_ip_interface module parser."""

from ipv4_show_ip_interface import _parse_ip_interface


def test_parse_entries():
    output = """\
Interface    IP Address    Subnet Mask     Admin Status  Oper. Status
-----------  ------------  --------------  ------------  ------------
vlan1        10.90.90.90   255.0.0.0       Up            Up
"""
    entries = _parse_ip_interface(output)
    assert len(entries) == 1
    assert entries[0]["interface"] == "vlan1"
    assert entries[0]["ip_address"] == "10.90.90.90"
    assert entries[0]["subnet_mask"] == "255.0.0.0"
    assert entries[0]["admin_status"] == "Up"
    assert entries[0]["oper_status"] == "Up"


def test_empty():
    output = """\
Interface    IP Address    Subnet Mask     Admin Status  Oper. Status
-----------  ------------  --------------  ------------  ------------
"""
    entries = _parse_ip_interface(output)
    assert entries == []
