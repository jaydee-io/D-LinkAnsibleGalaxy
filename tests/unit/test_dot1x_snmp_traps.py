"""Unit tests for dot1x_snmp_traps module command builder."""

from dot1x_snmp_traps import _build_command


def test_enable():
    assert _build_command("enabled") == "snmp-server enable traps dot1x"


def test_disable():
    assert _build_command("disabled") == "no snmp-server enable traps dot1x"
