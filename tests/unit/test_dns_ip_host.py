"""Unit tests for dns_ip_host module command builder."""

from dns_ip_host import _build_commands


def test_add():
    cmds = _build_commands("www.abc.com", "192.168.5.243", "present")
    assert cmds == ["ip host www.abc.com 192.168.5.243"]


def test_remove():
    cmds = _build_commands("www.abc.com", "192.168.5.243", "absent")
    assert cmds == ["no ip host www.abc.com 192.168.5.243"]
