"""Unit tests for mld_snooping_enable module."""

from mld_snooping_enable import _build_commands


def test_enable_global():
    assert _build_commands(None, "enabled") == ["ipv6 mld snooping"]


def test_disable_global():
    assert _build_commands(None, "disabled") == ["no ipv6 mld snooping"]


def test_enable_vlan():
    assert _build_commands(1, "enabled") == ["vlan 1", "ipv6 mld snooping", "exit"]


def test_disable_vlan():
    assert _build_commands(1, "disabled") == ["vlan 1", "no ipv6 mld snooping", "exit"]
