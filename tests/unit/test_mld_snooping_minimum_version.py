"""Unit tests for mld_snooping_minimum_version module."""

from mld_snooping_minimum_version import _build_commands


def test_enable():
    assert _build_commands(1, "enabled") == [
        "vlan 1", "ipv6 mld snooping minimum-version 2", "exit"]


def test_disable():
    assert _build_commands(1, "disabled") == [
        "vlan 1", "no ipv6 mld snooping minimum-version", "exit"]
