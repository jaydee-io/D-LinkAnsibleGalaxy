"""Unit tests for impb_snmp_traps module."""

from impb_snmp_traps import _build_commands


def test_enabled():
    assert _build_commands("enabled") == ["snmp-server enable traps ip-mac-port-binding"]


def test_disabled():
    assert _build_commands("disabled") == ["no snmp-server enable traps ip-mac-port-binding"]
