"""Unit tests for dhcp_snooping_clear_binding module command builder."""

from dhcp_snooping_clear_binding import _build_commands


def test_clear_all():
    cmds = _build_commands(None, None, None, None)
    assert cmds == ["clear ip dhcp snooping binding"]


def test_clear_by_mac():
    cmds = _build_commands("00:11:22:33:44:55", None, None, None)
    assert cmds == ["clear ip dhcp snooping binding 00:11:22:33:44:55"]


def test_clear_by_mac_ip_vlan_interface():
    cmds = _build_commands("00:11:22:33:44:55", "10.0.0.1", 100, "ethernet 1/0/1")
    assert cmds == ["clear ip dhcp snooping binding 00:11:22:33:44:55 10.0.0.1 vlan 100 interface ethernet 1/0/1"]
