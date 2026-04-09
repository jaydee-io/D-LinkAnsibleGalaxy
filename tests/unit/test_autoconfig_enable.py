"""Unit tests for autoconfig_enable module command builder."""

from autoconfig_enable import _build_commands


def test_enable():
    cmds = _build_commands("enabled")
    assert cmds == ["autoconfig enable"]


def test_disable():
    cmds = _build_commands("disabled")
    assert cmds == ["no autoconfig enable"]
