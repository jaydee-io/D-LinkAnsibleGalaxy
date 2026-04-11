"""Unit tests for dhcpv6_relay_remote_id_policy module command builder."""

from dhcpv6_relay_remote_id_policy import _build_commands


def test_set_drop():
    cmds = _build_commands("drop", "present")
    assert cmds == ["ipv6 dhcp relay remote-id policy drop"]


def test_set_keep():
    cmds = _build_commands("keep", "present")
    assert cmds == ["ipv6 dhcp relay remote-id policy keep"]


def test_reset():
    cmds = _build_commands(None, "absent")
    assert cmds == ["no ipv6 dhcp relay remote-id policy"]
