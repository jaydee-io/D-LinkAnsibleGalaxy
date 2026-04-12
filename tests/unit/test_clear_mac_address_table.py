"""Unit tests for clear_mac_address_table module."""

from clear_mac_address_table import _build_commands


def test_clear_all():
    assert _build_commands("all", None, None, None) == ["clear mac-address-table dynamic all"]


def test_clear_address():
    assert _build_commands("address", "00:08:00:70:00:07", None, None) == [
        "clear mac-address-table dynamic address 00:08:00:70:00:07"
    ]


def test_clear_interface():
    assert _build_commands("interface", None, "eth1/0/1", None) == [
        "clear mac-address-table dynamic interface eth1/0/1"
    ]


def test_clear_vlan():
    assert _build_commands("vlan", None, None, 10) == ["clear mac-address-table dynamic vlan 10"]
