"""Unit tests for show_snmp_server module command builder."""

from show_snmp_server import _build_command


def test_show_server():
    assert _build_command(False) == "show snmp-server"


def test_show_traps():
    assert _build_command(True) == "show snmp-server traps"
