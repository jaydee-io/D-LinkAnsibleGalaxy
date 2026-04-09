"""Unit tests for aaa_tacacs_server_host module command builder."""

from aaa_tacacs_server_host import _build_commands


def test_basic():
    cmds = _build_commands("192.168.1.200", None, None, "mysecret", None, "present")
    assert cmds == ["tacacs-server host 192.168.1.200 key mysecret"]


def test_full():
    cmds = _build_commands("192.168.1.200", 49, 5, "mysecret", 7, "present")
    assert cmds == ["tacacs-server host 192.168.1.200 port 49 timeout 5 key 7 mysecret"]


def test_absent():
    cmds = _build_commands("192.168.1.200", None, None, None, None, "absent")
    assert cmds == ["no tacacs-server host 192.168.1.200"]
