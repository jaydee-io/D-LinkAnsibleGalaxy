"""Unit tests for dgs1250_command module command builder."""

from dgs1250_command import _build_commands


def test_single_command():
    cmds = _build_commands(["show vlan"])
    assert cmds == ["show vlan"]


def test_multiple_commands():
    cmds = _build_commands(["interface ethernet 1/0/1", "description Uplink", "exit"])
    assert cmds == ["interface ethernet 1/0/1", "description Uplink", "exit"]


def test_passthrough():
    original = ["cmd1", "cmd2", "cmd3"]
    cmds = _build_commands(original)
    assert cmds == original
    assert cmds is not original
