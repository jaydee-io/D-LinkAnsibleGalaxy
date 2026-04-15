"""Unit tests for mld_snooping_static_group module."""

from mld_snooping_static_group import _build_commands


def test_add():
    assert _build_commands(1, "FF02::12:03", "eth1/0/5", "present") == [
        "vlan 1", "ipv6 mld snooping static-group FF02::12:03 interface eth1/0/5", "exit"]


def test_remove():
    assert _build_commands(1, "FF02::12:03", None, "absent") == [
        "vlan 1", "no ipv6 mld snooping static-group FF02::12:03", "exit"]
