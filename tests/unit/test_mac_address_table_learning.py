"""Unit tests for mac_address_table_learning module."""

from mac_address_table_learning import _build_commands


def test_present():
    assert _build_commands("eth1/0/5", "present") == ["mac-address-table learning interface eth1/0/5"]


def test_absent():
    assert _build_commands("eth1/0/1-8", "absent") == ["no mac-address-table learning interface eth1/0/1-8"]
