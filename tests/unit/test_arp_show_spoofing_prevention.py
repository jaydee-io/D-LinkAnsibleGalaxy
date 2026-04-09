"""Unit tests for arp_show_spoofing_prevention module parser."""

from arp_show_spoofing_prevention import _parse_entries


def test_single_entry():
    output = """\
IP               MAC                Interfaces
---------------- ------------------ ----------------------------
10.254.254.251   00-00-00-11-11-11  eth1/0/10

Total Entries: 1
"""
    entries, total = _parse_entries(output)
    assert len(entries) == 1
    assert entries[0]["ip"] == "10.254.254.251"
    assert entries[0]["mac"] == "00-00-00-11-11-11"
    assert entries[0]["interfaces"] == "eth1/0/10"
    assert total == 1


def test_multiple_entries():
    output = """\
IP               MAC                Interfaces
---------------- ------------------ ----------------------------
10.254.254.251   00-00-00-11-11-11  eth1/0/10
192.168.1.1      AA-BB-CC-DD-EE-FF  eth1/0/1,eth1/0/2

Total Entries: 2
"""
    entries, total = _parse_entries(output)
    assert len(entries) == 2
    assert entries[1]["ip"] == "192.168.1.1"
    assert entries[1]["interfaces"] == "eth1/0/1,eth1/0/2"
    assert total == 2


def test_empty():
    output = """\
IP               MAC                Interfaces
---------------- ------------------ ----------------------------

Total Entries: 0
"""
    entries, total = _parse_entries(output)
    assert entries == []
    assert total == 0


def test_no_output():
    entries, total = _parse_entries("")
    assert entries == []
    assert total == 0
