"""Unit tests for cable_diag_clear module command builder."""

from cable_diag_clear import _build_commands


def test_all():
    cmds = _build_commands("all", None)
    assert cmds == ["clear cable-diagnostics all"]


def test_interface():
    cmds = _build_commands("interface", "eth1/0/1")
    assert cmds == ["clear cable-diagnostics interface eth1/0/1"]
