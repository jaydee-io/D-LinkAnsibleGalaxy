"""Unit tests for voice_vlan_qos module."""

from voice_vlan_qos import _build_commands


def test_set():
    assert _build_commands(7, "present") == ["voice vlan qos 7"]


def test_absent():
    assert _build_commands(None, "absent") == ["no voice vlan qos"]
