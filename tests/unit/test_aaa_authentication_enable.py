"""Unit tests for aaa_authentication_enable module command builder."""

from aaa_authentication_enable import _build_commands


def test_present():
    cmds = _build_commands(["group group2"], "present")
    assert cmds == ["aaa authentication enable default group group2"]


def test_absent():
    cmds = _build_commands(None, "absent")
    assert cmds == ["no aaa authentication enable default"]
