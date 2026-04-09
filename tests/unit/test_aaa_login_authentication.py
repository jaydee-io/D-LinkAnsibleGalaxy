"""Unit tests for aaa_login_authentication module command builder."""

from aaa_login_authentication import _build_commands


def test_present_console_default():
    cmds = _build_commands("console", "default", "present")
    assert cmds == ["line console", "login authentication default", "exit"]


def test_present_telnet_named():
    cmds = _build_commands("telnet", "MY_LIST", "present")
    assert cmds == ["line telnet", "login authentication MY_LIST", "exit"]


def test_absent():
    cmds = _build_commands("ssh", "default", "absent")
    assert cmds == ["line ssh", "no login authentication", "exit"]
