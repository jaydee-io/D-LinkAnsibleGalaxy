"""Unit tests for dhcp_snooping_server_screen_profile module command builder."""

from dhcp_snooping_server_screen_profile import _build_commands


def test_create():
    cmds = _build_commands("myprofile", "present")
    assert cmds == ["dhcp-server-screen profile myprofile"]


def test_remove():
    cmds = _build_commands("myprofile", "absent")
    assert cmds == ["no dhcp-server-screen profile myprofile"]
