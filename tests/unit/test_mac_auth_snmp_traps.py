"""Unit tests for mac_auth_snmp_traps module."""

from mac_auth_snmp_traps import _build_commands


def test_enable():
    assert _build_commands("enabled") == ["snmp-server enable traps mac-auth"]


def test_disable():
    assert _build_commands("disabled") == ["no snmp-server enable traps mac-auth"]
