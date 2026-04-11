"""Unit tests for dhcp_snooping_vlan module command builder."""

from dhcp_snooping_vlan import _build_commands


def test_add():
    cmds = _build_commands("100", "present")
    assert cmds == ["ip dhcp snooping vlan 100"]


def test_remove():
    cmds = _build_commands("100", "absent")
    assert cmds == ["no ip dhcp snooping vlan 100"]
