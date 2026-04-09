"""Unit tests for aaa_radius_attribute_4 module command builder."""

from aaa_radius_attribute_4 import _build_commands


def test_present():
    cmds = _build_commands("10.0.0.1", "present")
    assert cmds == ["radius-server attribute 4 10.0.0.1"]


def test_absent():
    cmds = _build_commands("10.0.0.1", "absent")
    assert cmds == ["no radius-server attribute 4 10.0.0.1"]
