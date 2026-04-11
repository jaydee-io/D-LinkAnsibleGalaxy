"""Unit tests for dhcp_relay_class module command builder."""

from dhcp_relay_class import _build_commands


def test_add_class():
    cmds = _build_commands("pool1", "Service-A", "present")
    assert cmds == ["ip dhcp pool pool1", "class Service-A", "exit"]


def test_remove_class():
    cmds = _build_commands("pool1", "Service-A", "absent")
    assert cmds == ["ip dhcp pool pool1", "no class Service-A", "exit"]
