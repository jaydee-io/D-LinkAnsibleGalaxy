"""Unit tests for aaa_client module command builder."""

from aaa_client import _build_commands


def test_present():
    cmds = _build_commands("192.168.1.100", "mysecret", None, "present")
    assert cmds == [
        "aaa server radius dynamic-author",
        "client 192.168.1.100 server-key mysecret",
        "exit",
    ]


def test_present_with_encryption():
    cmds = _build_commands("192.168.1.100", "mysecret", 7, "present")
    assert cmds == [
        "aaa server radius dynamic-author",
        "client 192.168.1.100 server-key 7 mysecret",
        "exit",
    ]


def test_absent():
    cmds = _build_commands("192.168.1.100", "mysecret", None, "absent")
    assert cmds == [
        "aaa server radius dynamic-author",
        "no client 192.168.1.100 server-key mysecret",
        "exit",
    ]
