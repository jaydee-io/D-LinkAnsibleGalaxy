"""Unit tests for dhcpv6_guard_attach_policy module command builder."""

from dhcpv6_guard_attach_policy import _build_commands


def test_attach_default():
    cmds = _build_commands("ethernet 1/0/1", None, "present")
    assert cmds == ["interface ethernet 1/0/1", "ipv6 dhcp guard attach-policy", "exit"]


def test_attach_named():
    cmds = _build_commands("ethernet 1/0/1", "my-policy", "present")
    assert cmds == ["interface ethernet 1/0/1", "ipv6 dhcp guard attach-policy my-policy", "exit"]


def test_detach():
    cmds = _build_commands("ethernet 1/0/1", None, "absent")
    assert cmds == ["interface ethernet 1/0/1", "no ipv6 dhcp guard attach-policy", "exit"]
