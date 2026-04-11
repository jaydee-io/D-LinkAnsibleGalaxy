"""Unit tests for dhcp_snooping_snmp_traps module command builder."""

from dhcp_snooping_snmp_traps import _build_commands


def test_enable():
    cmds = _build_commands("enabled")
    assert cmds == ["snmp-server enable traps dhcp-server-screen"]


def test_disable():
    cmds = _build_commands("disabled")
    assert cmds == ["no snmp-server enable traps dhcp-server-screen"]
