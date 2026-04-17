"""Unit tests for poe_snmp_traps module command builder."""

from poe_snmp_traps import _build_commands


def test_enable():
    assert _build_commands("enabled") == ["snmp-server enable traps poe"]


def test_disable():
    assert _build_commands("disabled") == ["no snmp-server enable traps poe"]
