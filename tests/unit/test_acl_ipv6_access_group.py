"""Unit tests for ipv6_access_group module command builder."""

from acl_ipv6_access_group import _build_commands


def test_apply():
    cmds = _build_commands("eth1/0/3", "ip6-control", "present")
    assert cmds == ["interface eth1/0/3", "ipv6 access-group ip6-control in"]


def test_remove():
    cmds = _build_commands("eth1/0/3", "ip6-control", "absent")
    assert cmds == ["interface eth1/0/3", "no ipv6 access-group ip6-control in"]
