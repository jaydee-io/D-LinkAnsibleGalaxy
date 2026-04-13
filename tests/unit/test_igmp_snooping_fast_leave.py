"""Unit tests for igmp_snooping_fast_leave module."""

from igmp_snooping_fast_leave import _build_commands


def test_enabled():
    assert _build_commands(1, "enabled") == ["vlan 1", "ip igmp snooping fast-leave", "exit"]


def test_disabled():
    assert _build_commands(1, "disabled") == ["vlan 1", "no ip igmp snooping fast-leave", "exit"]
