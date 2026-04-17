"""Unit tests for snmp_server_enable_traps_rmon module command builder."""

from snmp_server_enable_traps_rmon import _build_commands


def test_enable_all():
    assert _build_commands(None, "present") == [
        "snmp-server enable traps rmon",
    ]


def test_enable_rising():
    assert _build_commands("rising-alarm", "present") == [
        "snmp-server enable traps rmon rising-alarm",
    ]


def test_disable_all():
    assert _build_commands(None, "absent") == [
        "no snmp-server enable traps rmon",
    ]


def test_disable_falling():
    assert _build_commands("falling-alarm", "absent") == [
        "no snmp-server enable traps rmon falling-alarm",
    ]
