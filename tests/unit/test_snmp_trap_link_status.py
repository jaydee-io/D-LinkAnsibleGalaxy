"""Unit tests for snmp_trap_link_status module command builder."""

from snmp_trap_link_status import _build_commands


def test_enable():
    assert _build_commands("eth1/0/1", "enabled") == [
        "interface eth1/0/1",
        "snmp trap link-status",
        "exit",
    ]


def test_disable():
    assert _build_commands("eth1/0/1", "disabled") == [
        "interface eth1/0/1",
        "no snmp trap link-status",
        "exit",
    ]
