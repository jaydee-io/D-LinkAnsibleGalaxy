"""Unit tests for debug_clear_error_log module command builder."""

from debug_clear_error_log import _build_commands


def test_build_commands():
    cmds = _build_commands()
    assert cmds == ["debug clear error-log"]
