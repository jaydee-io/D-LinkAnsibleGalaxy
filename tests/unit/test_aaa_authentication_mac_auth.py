"""Unit tests for aaa_authentication_mac_auth module command builder."""

from aaa_authentication_mac_auth import _build_commands


def test_present():
    cmds = _build_commands(["group radius"], "present")
    assert cmds == ["aaa authentication mac-auth default group radius"]


def test_absent():
    cmds = _build_commands(None, "absent")
    assert cmds == ["no aaa authentication mac-auth default"]
