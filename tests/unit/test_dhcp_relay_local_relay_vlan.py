"""Unit tests for dhcp_relay_local_relay_vlan module command builder."""

from dhcp_relay_local_relay_vlan import _build_commands


def test_enable():
    cmds = _build_commands("100", "present")
    assert cmds == ["ip dhcp local-relay vlan 100"]


def test_disable():
    cmds = _build_commands("100", "absent")
    assert cmds == ["no ip dhcp local-relay vlan 100"]


def test_range():
    cmds = _build_commands("10,15-18", "present")
    assert cmds == ["ip dhcp local-relay vlan 10,15-18"]
