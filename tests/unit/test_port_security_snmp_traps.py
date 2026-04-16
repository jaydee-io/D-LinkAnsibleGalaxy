"""Unit tests for port_security_snmp_traps module command builder."""

from port_security_snmp_traps import _build_commands


def test_enable():
    assert _build_commands(None, "enabled") == ["snmp-server enable traps port-security"]


def test_enable_with_rate():
    assert _build_commands(3, "enabled") == [
        "snmp-server enable traps port-security trap-rate 3"
    ]


def test_disable():
    assert _build_commands(None, "disabled") == ["no snmp-server enable traps port-security"]
