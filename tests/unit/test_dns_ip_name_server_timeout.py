"""Unit tests for dns_ip_name_server_timeout module command builder."""

from dns_ip_name_server_timeout import _build_commands


def test_set():
    cmds = _build_commands(5, "present")
    assert cmds == ["ip name-server timeout 5"]


def test_remove():
    cmds = _build_commands(None, "absent")
    assert cmds == ["no ip name-server timeout"]
