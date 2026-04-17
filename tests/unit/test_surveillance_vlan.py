"""Unit tests for surveillance_vlan module."""

from surveillance_vlan import _build_commands


def test_set():
    assert _build_commands(1001, "present") == ["surveillance vlan 1001"]


def test_remove():
    assert _build_commands(None, "absent") == ["no surveillance vlan"]
