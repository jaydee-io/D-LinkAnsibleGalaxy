"""Unit tests for ipv6_access_list module command builder."""

from acl_ipv6_access_list import _build_commands


def test_create_extended():
    cmds = _build_commands("ip6-control", None, True, "present")
    assert cmds == ["ipv6 access-list extended ip6-control", "exit"]


def test_create_standard():
    cmds = _build_commands("ip6-std-control", None, False, "present")
    assert cmds == ["ipv6 access-list ip6-std-control", "exit"]


def test_create_with_number():
    cmds = _build_commands("ip6-control", 13000, True, "present")
    assert cmds == ["ipv6 access-list extended ip6-control 13000", "exit"]


def test_delete():
    cmds = _build_commands("ip6-control", None, True, "absent")
    assert cmds == ["no ipv6 access-list extended ip6-control"]
