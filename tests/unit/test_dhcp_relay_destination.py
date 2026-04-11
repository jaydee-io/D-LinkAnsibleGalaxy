"""Unit tests for dhcp_relay_destination module command builder."""

from dhcp_relay_destination import _build_commands


def test_add():
    cmds = _build_commands("pool1", "10.2.1.1", "present")
    assert cmds == ["ip dhcp pool pool1", "relay destination 10.2.1.1", "exit"]


def test_remove():
    cmds = _build_commands("pool1", "10.2.1.1", "absent")
    assert cmds == ["ip dhcp pool pool1", "no relay destination 10.2.1.1", "exit"]
