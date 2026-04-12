"""Unit tests for mac_address_table_static module."""

from mac_address_table_static import _build_commands


def test_present_with_interface():
    assert _build_commands("C2:F3:22:0A:12:F4", 4, "eth1/0/1", False, False, "present") == [
        "mac-address-table static C2:F3:22:0A:12:F4 vlan 4 interface eth1/0/1"
    ]


def test_present_with_drop():
    assert _build_commands("00:01:00:02:00:07", 6, None, True, False, "present") == [
        "mac-address-table static 00:01:00:02:00:07 vlan 6 drop"
    ]


def test_absent_specific():
    assert _build_commands("C2:F3:22:0A:12:F4", 4, None, False, False, "absent") == [
        "no mac-address-table static C2:F3:22:0A:12:F4 vlan 4"
    ]


def test_absent_all():
    assert _build_commands(None, None, None, False, True, "absent") == [
        "no mac-address-table static all"
    ]
