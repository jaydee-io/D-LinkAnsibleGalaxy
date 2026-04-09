"""Unit tests for aaa_radius_deadtime module command builder."""

from aaa_radius_deadtime import _build_commands


def test_present():
    cmds = _build_commands(10, "present")
    assert cmds == ["radius-server deadtime 10"]


def test_absent():
    cmds = _build_commands(None, "absent")
    assert cmds == ["no radius-server deadtime"]
