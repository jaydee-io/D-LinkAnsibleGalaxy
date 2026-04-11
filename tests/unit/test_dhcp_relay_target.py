"""Unit tests for dhcp_relay_target module command builder."""

from dhcp_relay_target import _build_commands


def test_add():
    cmds = _build_commands("pool1", "10.2.1.2", "present")
    assert cmds == ["ip dhcp pool pool1", "relay target 10.2.1.2", "exit"]


def test_remove():
    cmds = _build_commands("pool1", "10.2.1.2", "absent")
    assert cmds == ["ip dhcp pool pool1", "no relay target 10.2.1.2", "exit"]
