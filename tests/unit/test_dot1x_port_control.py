"""Unit tests for dot1x_port_control module command builder."""

from dot1x_port_control import _build_commands


def test_set_auto():
    cmds = _build_commands("eth1/0/1", "present", "auto")
    assert cmds == ["interface eth1/0/1", "dot1x port-control auto"]


def test_set_force_authorized():
    cmds = _build_commands("eth1/0/1", "present", "force-authorized")
    assert cmds == ["interface eth1/0/1", "dot1x port-control force-authorized"]


def test_set_force_unauthorized():
    cmds = _build_commands("eth1/0/1", "present", "force-unauthorized")
    assert cmds == ["interface eth1/0/1", "dot1x port-control force-unauthorized"]


def test_reset_to_default():
    cmds = _build_commands("eth1/0/1", "absent", None)
    assert cmds == ["interface eth1/0/1", "no dot1x port-control"]
