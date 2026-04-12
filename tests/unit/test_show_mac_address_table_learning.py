"""Unit tests for show_mac_address_table_learning module."""

from show_mac_address_table_learning import _build_command


def test_all_interfaces():
    assert _build_command(None) == "show mac-address-table learning"


def test_specific_interface():
    assert _build_command("eth1/0/1-10") == "show mac-address-table learning interface eth1/0/1-10"
