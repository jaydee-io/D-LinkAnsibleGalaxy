"""Unit tests for aaa_server_tacacs module command builder."""

from aaa_server_tacacs import _build_commands


def test_present():
    cmds = _build_commands("my_group", "192.168.1.200", "present")
    assert cmds == [
        "aaa group server tacacs+ my_group",
        "server 192.168.1.200",
        "exit",
    ]


def test_absent():
    cmds = _build_commands("my_group", "192.168.1.200", "absent")
    assert cmds == [
        "aaa group server tacacs+ my_group",
        "no server 192.168.1.200",
        "exit",
    ]
