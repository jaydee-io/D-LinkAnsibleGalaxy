"""Unit tests for voice_vlan_enable module."""

from voice_vlan_enable import _build_commands


def test_enable():
    assert _build_commands("eth1/0/1", "enabled") == [
        "interface eth1/0/1", "voice vlan enable", "exit"]


def test_disable():
    assert _build_commands("eth1/0/1", "disabled") == [
        "interface eth1/0/1", "no voice vlan enable", "exit"]
