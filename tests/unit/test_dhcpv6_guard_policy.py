"""Unit tests for dhcpv6_guard_policy module command builder."""

from dhcpv6_guard_policy import _build_commands


def test_create():
    cmds = _build_commands("my-policy", "present")
    assert cmds == ["ipv6 dhcp guard policy my-policy"]


def test_remove():
    cmds = _build_commands("my-policy", "absent")
    assert cmds == ["no ipv6 dhcp guard policy my-policy"]
