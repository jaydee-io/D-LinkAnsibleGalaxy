"""Unit tests for dai_ip_arp_inspection_vlan_logging module command builder."""

from dai_ip_arp_inspection_vlan_logging import _build_commands


def test_acl_match_all():
    cmds = _build_commands("1", "acl-match", "all", "present")
    assert cmds == ["ip arp inspection vlan 1 logging acl-match all"]


def test_dhcp_bindings_none():
    cmds = _build_commands("1", "dhcp-bindings", "none", "present")
    assert cmds == ["ip arp inspection vlan 1 logging dhcp-bindings none"]


def test_remove():
    cmds = _build_commands("1", "acl-match", None, "absent")
    assert cmds == ["no ip arp inspection vlan 1 logging acl-match"]
