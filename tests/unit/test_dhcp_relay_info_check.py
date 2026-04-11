"""Unit tests for dhcp_relay_info_check module command builder."""

from dhcp_relay_info_check import _build_commands


def test_enable():
    cmds = _build_commands("enabled")
    assert cmds == ["ip dhcp relay information check"]


def test_disable():
    cmds = _build_commands("disabled")
    assert cmds == ["no ip dhcp relay information check"]
