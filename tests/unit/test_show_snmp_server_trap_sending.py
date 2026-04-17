"""Unit tests for show_snmp_server_trap_sending module command builder."""

from show_snmp_server_trap_sending import _build_command


def test_show_all():
    assert _build_command(None) == "show snmp-server trap-sending"


def test_show_interface():
    assert _build_command("eth1/0/1-9") == "show snmp-server trap-sending interface eth1/0/1-9"
