"""Unit tests for aaa_new_model module command builder."""

from aaa_new_model import _build_commands


def test_enable():
    cmds = _build_commands("enabled")
    assert cmds == ["aaa new-model"]


def test_disable():
    cmds = _build_commands("disabled")
    assert cmds == ["no aaa new-model"]
