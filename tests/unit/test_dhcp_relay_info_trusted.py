"""Unit tests for dhcp_relay_info_trusted module command builder."""

from dhcp_relay_info_trusted import _build_commands


def test_enable():
    cmds = _build_commands("vlan 100", "enabled")
    assert cmds == ["interface vlan 100", "ip dhcp relay information trusted", "exit"]


def test_disable():
    cmds = _build_commands("vlan 100", "disabled")
    assert cmds == ["interface vlan 100", "no ip dhcp relay information trusted", "exit"]
