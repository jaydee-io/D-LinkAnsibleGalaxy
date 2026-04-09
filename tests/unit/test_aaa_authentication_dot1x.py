"""Unit tests for aaa_authentication_dot1x module command builder."""

from aaa_authentication_dot1x import _build_commands


def test_present():
    cmds = _build_commands(["group radius"], "present")
    assert cmds == ["aaa authentication dot1x default group radius"]


def test_absent():
    cmds = _build_commands(None, "absent")
    assert cmds == ["no aaa authentication dot1x default"]
