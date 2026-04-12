"""Unit tests for show_mac_address_table_notification_change module."""

from show_mac_address_table_notification_change import _build_command


def test_global_config():
    assert _build_command(None, False) == "show mac-address-table notification change"


def test_history():
    assert _build_command(None, True) == "show mac-address-table notification change history"


def test_all_interfaces():
    assert _build_command("", False) == "show mac-address-table notification change interface"


def test_specific_interface():
    assert _build_command("eth1/0/1", False) == (
        "show mac-address-table notification change interface eth1/0/1"
    )
