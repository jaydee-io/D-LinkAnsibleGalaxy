"""Unit tests for vlan module."""

from vlan import _build_commands


def test_create():
    assert _build_commands("1000-1005", "present") == ["vlan 1000-1005", "exit"]


def test_delete():
    assert _build_commands("1000", "absent") == ["no vlan 1000"]
