"""Unit tests for snmp_server module command builder."""

from snmp_server import _build_commands


def test_enable():
    assert _build_commands("enabled") == [
        "snmp-server",
    ]


def test_disable():
    assert _build_commands("disabled") == [
        "no snmp-server",
    ]
