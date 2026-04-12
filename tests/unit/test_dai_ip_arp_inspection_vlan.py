"""Unit tests for dai_ip_arp_inspection_vlan module command builder."""

from dai_ip_arp_inspection_vlan import _build_commands


def test_enable():
    cmds = _build_commands("2", "present")
    assert cmds == ["ip arp inspection vlan 2"]


def test_disable():
    cmds = _build_commands("2", "absent")
    assert cmds == ["no ip arp inspection vlan 2"]
