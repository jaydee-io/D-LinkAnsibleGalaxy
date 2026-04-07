"""Unit tests for ip_access_group module command builder."""

from acl_ip_access_group import _build_commands


def test_apply():
    cmds = _build_commands("eth1/0/2", "Strict-Control", "present")
    assert cmds == ["interface eth1/0/2", "ip access-group Strict-Control in"]


def test_remove():
    cmds = _build_commands("eth1/0/2", "Strict-Control", "absent")
    assert cmds == ["interface eth1/0/2", "no ip access-group Strict-Control in"]
