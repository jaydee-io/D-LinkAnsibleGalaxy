"""Unit tests for igmp_snooping_querier module."""

from igmp_snooping_querier import _build_commands


def test_enabled():
    assert _build_commands(1, "enabled") == ["vlan 1", "ip igmp snooping querier", "exit"]


def test_disabled():
    assert _build_commands(1, "disabled") == ["vlan 1", "no ip igmp snooping querier", "exit"]
