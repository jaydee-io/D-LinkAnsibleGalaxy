"""Unit tests for show_snmp_trap_link_status module command builder."""

from show_snmp_trap_link_status import _build_command


def test_show_all():
    assert _build_command(None) == "show snmp trap link-status"


def test_show_interface():
    assert _build_command("eth1/0/1-9") == "show snmp trap link-status interface eth1/0/1-9"
