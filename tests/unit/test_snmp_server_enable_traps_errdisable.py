"""Unit tests for snmp_server_enable_traps_errdisable module."""

from snmp_server_enable_traps_errdisable import _build_commands


def test_present_no_options():
    assert _build_commands(None, None, None, "present") == ["snmp-server enable traps errdisable"]


def test_present_asserted_cleared():
    cmds = _build_commands(True, True, 3, "present")
    assert cmds == ["snmp-server enable traps errdisable asserted cleared notification-rate 3"]


def test_present_asserted_only():
    assert _build_commands(True, None, None, "present") == ["snmp-server enable traps errdisable asserted"]


def test_absent_no_options():
    assert _build_commands(None, None, None, "absent") == ["no snmp-server enable traps errdisable"]


def test_absent_with_notification_rate():
    assert _build_commands(None, None, 5, "absent") == ["no snmp-server enable traps errdisable notification-rate"]
