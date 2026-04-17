"""Unit tests for snmp_server_enable_traps module command builder."""

from snmp_server_enable_traps import _build_commands


def test_enable():
    assert _build_commands("enabled") == [
        "snmp-server enable traps",
    ]


def test_disable():
    assert _build_commands("disabled") == [
        "no snmp-server enable traps",
    ]
