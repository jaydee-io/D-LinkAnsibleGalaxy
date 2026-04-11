"""Unit tests for dhcp_relay_info_option_insert module command builder."""

from dhcp_relay_info_option_insert import _build_commands


def test_enable():
    cmds = _build_commands("vlan 100", False, "present")
    assert cmds == ["interface vlan 100", "ip dhcp relay information option-insert", "exit"]


def test_enable_none():
    cmds = _build_commands("vlan 100", True, "present")
    assert cmds == ["interface vlan 100", "ip dhcp relay information option-insert none", "exit"]


def test_disable():
    cmds = _build_commands("vlan 100", False, "absent")
    assert cmds == ["interface vlan 100", "no ip dhcp relay information option-insert", "exit"]
