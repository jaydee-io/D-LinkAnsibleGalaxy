"""Unit tests for debug_reboot_on_error module command builder."""

from debug_reboot_on_error import _build_commands


def test_enable():
    cmds = _build_commands("enabled")
    assert cmds == ["debug reboot on-error"]


def test_disable():
    cmds = _build_commands("disabled")
    assert cmds == ["no debug reboot on-error"]
