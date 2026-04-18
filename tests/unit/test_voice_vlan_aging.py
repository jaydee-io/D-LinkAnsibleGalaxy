"""Unit tests for voice_vlan_aging module."""

from voice_vlan_aging import _build_commands


def test_set():
    assert _build_commands(30, "present") == ["voice vlan aging 30"]


def test_absent():
    assert _build_commands(None, "absent") == ["no voice vlan aging"]
