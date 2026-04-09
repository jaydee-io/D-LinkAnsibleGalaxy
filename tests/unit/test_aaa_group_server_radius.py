"""Unit tests for aaa_group_server_radius module command builder."""

from aaa_group_server_radius import _build_commands


def test_present():
    cmds = _build_commands("my_radius_group", "present")
    assert cmds == ["aaa group server radius my_radius_group", "exit"]


def test_absent():
    cmds = _build_commands("my_radius_group", "absent")
    assert cmds == ["no aaa group server radius my_radius_group"]
