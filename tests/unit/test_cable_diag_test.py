"""Unit tests for cable_diag_test module command builder."""

from cable_diag_test import _build_commands


def test_interface():
    cmds = _build_commands("eth1/0/1")
    assert cmds == ["test cable-diagnostics interface eth1/0/1"]


def test_another_interface():
    cmds = _build_commands("eth1/0/5")
    assert cmds == ["test cable-diagnostics interface eth1/0/5"]
