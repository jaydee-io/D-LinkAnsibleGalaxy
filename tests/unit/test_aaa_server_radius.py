"""Unit tests for aaa_server_radius module command builder."""

from aaa_server_radius import _build_commands


def test_present():
    cmds = _build_commands("my_group", "192.168.1.100", "present")
    assert cmds == [
        "aaa group server radius my_group",
        "server 192.168.1.100",
        "exit",
    ]


def test_absent():
    cmds = _build_commands("my_group", "192.168.1.100", "absent")
    assert cmds == [
        "aaa group server radius my_group",
        "no server 192.168.1.100",
        "exit",
    ]
