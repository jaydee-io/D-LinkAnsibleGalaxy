"""Unit tests for aaa_accounting_network module command builder."""

from aaa_accounting_network import _build_commands


def test_present():
    cmds = _build_commands(["group radius"], "present")
    assert cmds == ["aaa accounting network default start-stop group radius"]


def test_none():
    cmds = _build_commands(["none"], "present")
    assert cmds == ["aaa accounting network default none"]


def test_absent():
    cmds = _build_commands(None, "absent")
    assert cmds == ["no aaa accounting network default"]
