"""Unit tests for aaa_port module command builder."""

from aaa_port import _build_commands


def test_present():
    cmds = _build_commands(1650, "present")
    assert cmds == ["aaa server radius dynamic-author", "port 1650", "exit"]


def test_absent():
    cmds = _build_commands(None, "absent")
    assert cmds == ["aaa server radius dynamic-author", "no port", "exit"]
