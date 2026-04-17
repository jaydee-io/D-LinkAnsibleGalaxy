"""Unit tests for surveillance_vlan_enable module."""

from surveillance_vlan_enable import _build_commands


def test_enable():
    assert _build_commands("eth1/0/1", "enabled") == [
        "interface eth1/0/1", "surveillance vlan enable", "exit"]


def test_disable():
    assert _build_commands("eth1/0/1", "disabled") == [
        "interface eth1/0/1", "no surveillance vlan enable", "exit"]
