"""Unit tests for surveillance_vlan_aging module."""

from surveillance_vlan_aging import _build_commands


def test_set():
    assert _build_commands(30, "present") == ["surveillance vlan aging 30"]


def test_reset():
    assert _build_commands(None, "absent") == ["no surveillance vlan aging"]
