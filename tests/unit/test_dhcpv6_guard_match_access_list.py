"""Unit tests for dhcpv6_guard_match_access_list module command builder."""

from dhcpv6_guard_match_access_list import _build_commands


def test_set():
    cmds = _build_commands("my-policy", "my-acl", "present")
    assert cmds == ["ipv6 dhcp guard policy my-policy", "match ipv6 access-list my-acl", "exit"]


def test_remove():
    cmds = _build_commands("my-policy", None, "absent")
    assert cmds == ["ipv6 dhcp guard policy my-policy", "no match ipv6 access-list", "exit"]
