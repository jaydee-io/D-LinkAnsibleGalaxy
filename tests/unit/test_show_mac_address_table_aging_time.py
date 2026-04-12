"""Unit tests for show_mac_address_table_aging_time module."""

from show_mac_address_table_aging_time import _build_command


def test_build_command():
    assert _build_command() == "show mac-address-table aging-time"
