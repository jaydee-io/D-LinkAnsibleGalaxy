"""Unit tests for dai_ip_arp_inspection_filter_vlan module command builder."""

from dai_ip_arp_inspection_filter_vlan import _build_commands


def test_add():
    cmds = _build_commands("static-arp-list", "10", False, "present")
    assert cmds == ["ip arp inspection filter static-arp-list vlan 10"]


def test_add_static():
    cmds = _build_commands("static-arp-list", "10", True, "present")
    assert cmds == ["ip arp inspection filter static-arp-list vlan 10 static"]


def test_remove():
    cmds = _build_commands("static-arp-list", "10", False, "absent")
    assert cmds == ["no ip arp inspection filter static-arp-list vlan 10"]
