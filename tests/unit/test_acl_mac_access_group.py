"""Unit tests for mac_access_group module command builder."""

from acl_mac_access_group import _build_commands


def test_apply():
    cmds = _build_commands("eth1/0/4", "daily-profile", "present")
    assert cmds == ["interface eth1/0/4", "mac access-group daily-profile in"]


def test_remove():
    cmds = _build_commands("eth1/0/4", "daily-profile", "absent")
    assert cmds == ["interface eth1/0/4", "no mac access-group daily-profile in"]
