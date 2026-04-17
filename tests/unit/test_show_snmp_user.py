"""Unit tests for show_snmp_user module command builder."""

from show_snmp_user import _build_command


def test_show_all():
    assert _build_command(None) == "show snmp user"


def test_show_specific():
    assert _build_command("authuser") == "show snmp user authuser"
