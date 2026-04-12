"""Unit tests for snmp_server_enable_traps_gratuitous_arp module."""

from snmp_server_enable_traps_gratuitous_arp import _build_commands


def test_present():
    assert _build_commands("present") == ["snmp-server enable traps gratuitous-arp"]


def test_absent():
    assert _build_commands("absent") == ["no snmp-server enable traps gratuitous-arp"]
