"""Unit tests for snmp_server_enable_traps_safeguard_engine module command builder."""

from snmp_server_enable_traps_safeguard_engine import _build_commands


def test_enable():
    assert _build_commands("enabled") == [
        "snmp-server enable traps safeguard-engine",
    ]


def test_disable():
    assert _build_commands("disabled") == [
        "no snmp-server enable traps safeguard-engine",
    ]
