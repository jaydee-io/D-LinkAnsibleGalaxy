"""Unit tests for dot1x_default module command builder."""

from dot1x_default import _build_commands


def test_build_commands():
    cmds = _build_commands("eth1/0/1")
    assert cmds == ["interface eth1/0/1", "dot1x default"]


def test_different_interface():
    cmds = _build_commands("eth1/0/24")
    assert cmds == ["interface eth1/0/24", "dot1x default"]
