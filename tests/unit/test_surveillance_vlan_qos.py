"""Unit tests for surveillance_vlan_qos module."""

from surveillance_vlan_qos import _build_commands


def test_set():
    assert _build_commands(7, "present") == ["surveillance vlan qos 7"]


def test_reset():
    assert _build_commands(None, "absent") == ["no surveillance vlan qos"]
