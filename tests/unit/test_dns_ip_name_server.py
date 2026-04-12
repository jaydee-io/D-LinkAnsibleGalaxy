"""Unit tests for dns_ip_name_server module command builder."""

from dns_ip_name_server import _build_commands


def test_add_single():
    cmds = _build_commands("192.168.5.134", None, "present")
    assert cmds == ["ip name-server 192.168.5.134"]


def test_add_two():
    cmds = _build_commands("192.168.5.134", "5001:5::2", "present")
    assert cmds == ["ip name-server 192.168.5.134 5001:5::2"]


def test_remove():
    cmds = _build_commands("192.168.5.134", None, "absent")
    assert cmds == ["no ip name-server 192.168.5.134"]
