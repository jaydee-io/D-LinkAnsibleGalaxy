"""Unit tests for aaa_group_server_tacacs module command builder."""

from aaa_group_server_tacacs import _build_commands


def test_present():
    cmds = _build_commands("my_tacacs_group", "present")
    assert cmds == ["aaa group server tacacs+ my_tacacs_group", "exit"]


def test_absent():
    cmds = _build_commands("my_tacacs_group", "absent")
    assert cmds == ["no aaa group server tacacs+ my_tacacs_group"]
