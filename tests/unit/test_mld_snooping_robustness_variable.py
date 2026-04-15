"""Unit tests for mld_snooping_robustness_variable module."""

from mld_snooping_robustness_variable import _build_commands


def test_set():
    assert _build_commands(1000, 3, "present") == [
        "vlan 1000", "ipv6 mld snooping robustness-variable 3", "exit"]


def test_reset():
    assert _build_commands(1000, None, "absent") == [
        "vlan 1000", "no ipv6 mld snooping robustness-variable", "exit"]
