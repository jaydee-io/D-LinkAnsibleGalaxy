"""Unit tests for aaa_server_radius_dynamic_author module command builder."""

from aaa_server_radius_dynamic_author import _build_commands


def test_enable():
    cmds = _build_commands("enabled")
    assert cmds == ["aaa server radius dynamic-author"]


def test_disable():
    cmds = _build_commands("disabled")
    assert cmds == ["no aaa server radius dynamic-author"]
