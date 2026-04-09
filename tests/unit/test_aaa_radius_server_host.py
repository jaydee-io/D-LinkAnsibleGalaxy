"""Unit tests for aaa_radius_server_host module command builder."""

from aaa_radius_server_host import _build_commands


def test_basic():
    cmds = _build_commands("192.168.1.100", None, None, None, None, "mysecret", None, "present")
    assert cmds == ["radius-server host 192.168.1.100 key mysecret"]


def test_full():
    cmds = _build_commands("192.168.1.100", 1812, 1813, 5, 3, "mysecret", 7, "present")
    assert cmds == [
        "radius-server host 192.168.1.100 auth-port 1812 acct-port 1813 timeout 5 retransmit 3 key 7 mysecret",
    ]


def test_absent():
    cmds = _build_commands("192.168.1.100", None, None, None, None, None, None, "absent")
    assert cmds == ["no radius-server host 192.168.1.100"]
