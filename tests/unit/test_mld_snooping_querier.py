"""Unit tests for mld_snooping_querier module."""

from mld_snooping_querier import _build_commands


def test_enable():
    assert _build_commands(1, "enabled") == ["vlan 1", "ipv6 mld snooping querier", "exit"]


def test_disable():
    assert _build_commands(1, "disabled") == ["vlan 1", "no ipv6 mld snooping querier", "exit"]
