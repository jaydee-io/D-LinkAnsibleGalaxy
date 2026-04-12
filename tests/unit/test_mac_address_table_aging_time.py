"""Unit tests for mac_address_table_aging_time module."""

from mac_address_table_aging_time import _build_commands


def test_present():
    assert _build_commands(200, "present") == ["mac-address-table aging-time 200"]


def test_present_zero():
    assert _build_commands(0, "present") == ["mac-address-table aging-time 0"]


def test_absent():
    assert _build_commands(None, "absent") == ["no mac-address-table aging-time"]
