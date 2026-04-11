"""Unit tests for dhcp_relay_ip_dhcp_pool module command builder."""

from dhcp_relay_ip_dhcp_pool import _build_commands


def test_create():
    cmds = _build_commands("pool1", "present")
    assert cmds == ["ip dhcp pool pool1"]


def test_delete():
    cmds = _build_commands("pool1", "absent")
    assert cmds == ["no ip dhcp pool pool1"]
