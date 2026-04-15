"""Unit tests for mld_snooping_fast_leave module."""

from mld_snooping_fast_leave import _build_commands


def test_enable():
    assert _build_commands(1, "enabled") == ["vlan 1", "ipv6 mld snooping fast-leave", "exit"]


def test_disable():
    assert _build_commands(1, "disabled") == ["vlan 1", "no ipv6 mld snooping fast-leave", "exit"]
