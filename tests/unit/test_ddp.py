"""Unit tests for ddp module command builder."""

from ddp import _build_commands


def test_enable_global():
    cmds = _build_commands(None, "enabled")
    assert cmds == ["ddp"]


def test_disable_global():
    cmds = _build_commands(None, "disabled")
    assert cmds == ["no ddp"]


def test_enable_interface():
    cmds = _build_commands("eth1/0/1", "enabled")
    assert cmds == ["interface eth1/0/1", "ddp", "exit"]


def test_disable_interface():
    cmds = _build_commands("eth1/0/1", "disabled")
    assert cmds == ["interface eth1/0/1", "no ddp", "exit"]
