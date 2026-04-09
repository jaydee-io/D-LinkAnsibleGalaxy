"""Unit tests for aaa_authentication_login module command builder."""

from aaa_authentication_login import _build_commands


def test_default():
    cmds = _build_commands("default", ["group group2", "local"], "present")
    assert cmds == ["aaa authentication login default group group2 local"]


def test_named_list():
    cmds = _build_commands("MY_LIST", ["group radius"], "present")
    assert cmds == ["aaa authentication login MY_LIST group radius"]


def test_absent():
    cmds = _build_commands("default", None, "absent")
    assert cmds == ["no aaa authentication login default"]
