"""Unit tests for dot1x_max_req module command builder."""

from dot1x_max_req import _build_commands


def test_set_max_req():
    cmds = _build_commands("eth1/0/1", "present", 3)
    assert cmds == ["interface eth1/0/1", "dot1x max-req 3"]


def test_set_max_req_boundary():
    cmds = _build_commands("eth1/0/1", "present", 10)
    assert cmds == ["interface eth1/0/1", "dot1x max-req 10"]


def test_reset_to_default():
    cmds = _build_commands("eth1/0/1", "absent", None)
    assert cmds == ["interface eth1/0/1", "no dot1x max-req"]


def test_different_interface():
    cmds = _build_commands("eth1/0/24", "present", 5)
    assert cmds == ["interface eth1/0/24", "dot1x max-req 5"]
