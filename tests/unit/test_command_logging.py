"""Unit tests for command_logging module command builder."""

from command_logging import _build_commands


def test_enable():
    cmds = _build_commands("enabled")
    assert cmds == ["command logging enable"]


def test_disable():
    cmds = _build_commands("disabled")
    assert cmds == ["no command logging enable"]
