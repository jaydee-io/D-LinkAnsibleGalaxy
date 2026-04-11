"""Unit tests for dhcpv6_relay_local_relay_vlan module command builder."""

from dhcpv6_relay_local_relay_vlan import _build_commands


def test_enable():
    cmds = _build_commands("100", "present")
    assert cmds == ["ipv6 dhcp local-relay vlan 100"]


def test_disable():
    cmds = _build_commands("100", "absent")
    assert cmds == ["no ipv6 dhcp local-relay vlan 100"]
