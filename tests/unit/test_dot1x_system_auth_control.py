"""Unit tests for dot1x_system_auth_control module command builder."""

from dot1x_system_auth_control import _build_commands


def test_enable():
    cmds = _build_commands("enabled")
    assert cmds == ["dot1x system-auth-control"]


def test_disable():
    cmds = _build_commands("disabled")
    assert cmds == ["no dot1x system-auth-control"]
