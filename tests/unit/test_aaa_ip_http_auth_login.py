"""Unit tests for aaa_ip_http_auth_login module command builder."""

from aaa_ip_http_auth_login import _build_commands


def test_default():
    cmds = _build_commands("default", "present")
    assert cmds == ["ip http authentication aaa login-authentication default"]


def test_named():
    cmds = _build_commands("MY_LIST", "present")
    assert cmds == ["ip http authentication aaa login-authentication MY_LIST"]


def test_absent():
    cmds = _build_commands("default", "absent")
    assert cmds == ["no ip http authentication aaa login-authentication"]
