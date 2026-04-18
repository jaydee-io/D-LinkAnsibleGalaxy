"""Unit tests for voice_vlan module."""

from voice_vlan import _build_commands


def test_set():
    assert _build_commands(1000, "present") == ["voice vlan 1000"]


def test_absent():
    assert _build_commands(None, "absent") == ["no voice vlan"]
