"""Unit tests for snmp_trap_mac_notification_change module."""

from snmp_trap_mac_notification_change import _build_commands


def test_present_added():
    cmds = _build_commands("eth1/0/2", True, None, "present")
    assert cmds == ["interface eth1/0/2", "snmp trap mac-notification change added", "exit"]


def test_present_removed():
    cmds = _build_commands("eth1/0/2", None, True, "present")
    assert cmds == ["interface eth1/0/2", "snmp trap mac-notification change removed", "exit"]


def test_present_both():
    cmds = _build_commands("eth1/0/1", True, True, "present")
    assert "snmp trap mac-notification change added" in cmds
    assert "snmp trap mac-notification change removed" in cmds


def test_absent():
    cmds = _build_commands("eth1/0/2", None, None, "absent")
    assert cmds == ["interface eth1/0/2", "no snmp trap mac-notification change", "exit"]
