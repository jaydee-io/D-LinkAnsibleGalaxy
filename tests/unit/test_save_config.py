"""Unit tests for save_config module command builder."""

from save_config import _build_commands


def test_build_commands():
    cmds = _build_commands()
    assert cmds == ["copy running-config startup-config"]
