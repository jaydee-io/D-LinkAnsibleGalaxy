"""Unit tests for aaa_radius_attribute_32 module command builder."""

from aaa_radius_attribute_32 import _build_commands


def test_present():
    cmds = _build_commands("my-switch", "present")
    assert cmds == ["radius-server attribute 32 include-in-access-req my-switch"]


def test_absent():
    cmds = _build_commands(None, "absent")
    assert cmds == ["no radius-server attribute 32 include-in-access-req"]
