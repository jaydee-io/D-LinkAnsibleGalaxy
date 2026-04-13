"""Unit tests for igmp_snooping_enable module."""

from igmp_snooping_enable import _build_commands


def test_enable_global():
    assert _build_commands(None, "enabled") == ["ip igmp snooping"]


def test_disable_global():
    assert _build_commands(None, "disabled") == ["no ip igmp snooping"]


def test_enable_vlan():
    assert _build_commands(1, "enabled") == ["vlan 1", "ip igmp snooping", "exit"]


def test_disable_vlan():
    assert _build_commands(1, "disabled") == ["vlan 1", "no ip igmp snooping", "exit"]
