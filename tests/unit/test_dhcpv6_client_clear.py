"""Unit tests for dhcpv6_client_clear module command builder."""

from dhcpv6_client_clear import _build_commands


def test_clear_vlan1():
    cmds = _build_commands("vlan1")
    assert cmds == ["clear ipv6 dhcp client vlan1"]


def test_clear_vlan_100():
    cmds = _build_commands("vlan 100")
    assert cmds == ["clear ipv6 dhcp client vlan 100"]
