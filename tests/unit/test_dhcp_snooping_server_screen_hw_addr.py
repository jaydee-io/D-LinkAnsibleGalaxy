"""Unit tests for dhcp_snooping_server_screen_hw_addr module command builder."""

from dhcp_snooping_server_screen_hw_addr import _build_commands


def test_add():
    cmds = _build_commands("myprofile", "00:11:22:33:44:55", "present")
    assert cmds == ["dhcp-server-screen profile myprofile", "based-on hardware-address 00:11:22:33:44:55", "exit"]


def test_remove():
    cmds = _build_commands("myprofile", "00:11:22:33:44:55", "absent")
    assert cmds == ["dhcp-server-screen profile myprofile", "no based-on hardware-address 00:11:22:33:44:55", "exit"]
