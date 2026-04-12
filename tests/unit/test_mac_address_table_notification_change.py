"""Unit tests for mac_address_table_notification_change module."""

from mac_address_table_notification_change import _build_commands


def test_present_enable():
    cmds = _build_commands(None, None, None, "present")
    assert "mac-address-table notification change" in cmds


def test_present_with_interval():
    cmds = _build_commands(10, None, None, "present")
    assert "mac-address-table notification change interval 10" in cmds


def test_present_with_history_size():
    cmds = _build_commands(None, 500, None, "present")
    assert "mac-address-table notification change history-size 500" in cmds


def test_present_with_trap_type():
    cmds = _build_commands(None, None, "with-vlanid", "present")
    assert "mac-address-table notification change trap-type with-vlanid" in cmds


def test_absent():
    assert _build_commands(None, None, None, "absent") == ["no mac-address-table notification change"]


def test_absent_interval():
    assert _build_commands(10, None, None, "absent") == ["no mac-address-table notification change interval"]
