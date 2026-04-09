"""Unit tests for aaa_radius_attribute_55 module command builder."""

from aaa_radius_attribute_55 import _build_commands


def test_enable():
    cmds = _build_commands("enabled")
    assert cmds == ["radius-server attribute 55 include-in-acct-req"]


def test_disable():
    cmds = _build_commands("disabled")
    assert cmds == ["no radius-server attribute 55 include-in-acct-req"]
