"""Unit tests for snmp_server_trap_sending module command builder."""

from snmp_server_trap_sending import _build_commands


def test_disable():
    assert _build_commands("eth1/0/8", "disabled") == [
        "interface eth1/0/8",
        "snmp-server trap-sending disable",
        "exit",
    ]


def test_enable():
    assert _build_commands("eth1/0/8", "enabled") == [
        "interface eth1/0/8",
        "no snmp-server trap-sending disable",
        "exit",
    ]
