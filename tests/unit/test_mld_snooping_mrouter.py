"""Unit tests for mld_snooping_mrouter module."""

from mld_snooping_mrouter import _build_commands


def test_add_interface():
    assert _build_commands(1, "interface", "eth1/0/1", "present") == [
        "vlan 1", "ipv6 mld snooping mrouter interface eth1/0/1", "exit"]


def test_add_forbidden():
    assert _build_commands(1, "forbidden", "eth1/0/2", "present") == [
        "vlan 1", "ipv6 mld snooping mrouter forbidden interface eth1/0/2", "exit"]


def test_remove_interface():
    assert _build_commands(1, "interface", "eth1/0/1", "absent") == [
        "vlan 1", "no ipv6 mld snooping mrouter interface eth1/0/1", "exit"]


def test_disable_learn_pimv6():
    assert _build_commands(4, "learn-pimv6", None, "absent") == [
        "vlan 4", "no ipv6 mld snooping mrouter learn pimv6", "exit"]
