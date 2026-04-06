"""Unit tests for dot1x_forward_pdu module command builder."""

from dot1x_forward_pdu import _build_commands


def test_enable():
    cmds = _build_commands("eth1/0/1", "enabled")
    assert cmds == ["interface eth1/0/1", "dot1x forward-pdu"]


def test_disable():
    cmds = _build_commands("eth1/0/1", "disabled")
    assert cmds == ["interface eth1/0/1", "no dot1x forward-pdu"]


def test_different_interface():
    cmds = _build_commands("eth1/0/12", "enabled")
    assert cmds == ["interface eth1/0/12", "dot1x forward-pdu"]
