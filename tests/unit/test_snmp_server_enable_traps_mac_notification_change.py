"""Unit tests for snmp_server_enable_traps_mac_notification_change module."""

from snmp_server_enable_traps_mac_notification_change import _build_commands


def test_present():
    assert _build_commands("present") == ["snmp-server enable traps mac-notification change"]


def test_absent():
    assert _build_commands("absent") == ["no snmp-server enable traps mac-notification change"]
