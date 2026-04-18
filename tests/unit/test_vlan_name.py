"""Unit tests for vlan_name module."""

from vlan_name import _build_commands


def test_set():
    assert _build_commands(1000, "admin-vlan", "present") == [
        "vlan 1000", "name admin-vlan", "exit"]


def test_absent():
    assert _build_commands(1000, None, "absent") == [
        "vlan 1000", "no name", "exit"]
