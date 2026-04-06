"""Unit tests for dot1x_control_direction module command builder."""

from dot1x_control_direction import _build_commands


def test_set_direction_in():
    cmds = _build_commands("eth1/0/1", "present", "in")
    assert cmds == ["interface eth1/0/1", "dot1x control-direction in"]


def test_set_direction_both():
    cmds = _build_commands("eth1/0/1", "present", "both")
    assert cmds == ["interface eth1/0/1", "dot1x control-direction both"]


def test_reset_to_default():
    cmds = _build_commands("eth1/0/1", "absent", None)
    assert cmds == ["interface eth1/0/1", "no dot1x control-direction"]


def test_different_interface():
    cmds = _build_commands("eth1/0/24", "present", "in")
    assert cmds == ["interface eth1/0/24", "dot1x control-direction in"]
