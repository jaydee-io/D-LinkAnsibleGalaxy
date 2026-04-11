"""Unit tests for dhcpv6_relay_remote_id_option module command builder."""

from dhcpv6_relay_remote_id_option import _build_commands


def test_enable():
    cmds = _build_commands("enabled")
    assert cmds == ["ipv6 dhcp relay remote-id option"]


def test_disable():
    cmds = _build_commands("disabled")
    assert cmds == ["no ipv6 dhcp relay remote-id option"]
