"""Unit tests for dhcp_relay_source module command builder."""

from dhcp_relay_source import _build_commands


def test_add():
    cmds = _build_commands("pool1", "172.19.18.0", "255.255.255.0", "present")
    assert cmds == ["ip dhcp pool pool1", "relay source 172.19.18.0 255.255.255.0", "exit"]


def test_remove():
    cmds = _build_commands("pool1", "172.19.18.0", "255.255.255.0", "absent")
    assert cmds == ["ip dhcp pool pool1", "no relay source 172.19.18.0 255.255.255.0", "exit"]
