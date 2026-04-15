"""Unit tests for lldp_snmp_traps module."""

from lldp_snmp_traps import _build_commands


def test_enable_lldp():
    assert _build_commands(False, "enabled") == ["snmp-server enable traps lldp"]


def test_enable_med():
    assert _build_commands(True, "enabled") == ["snmp-server enable traps lldp med"]


def test_disable_lldp():
    assert _build_commands(False, "disabled") == ["no snmp-server enable traps lldp"]


def test_disable_med():
    assert _build_commands(True, "disabled") == ["no snmp-server enable traps lldp med"]
