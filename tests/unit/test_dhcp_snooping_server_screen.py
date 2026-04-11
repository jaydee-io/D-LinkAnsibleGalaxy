"""Unit tests for dhcp_snooping_server_screen module command builder."""

from dhcp_snooping_server_screen import _build_commands


def test_set_basic():
    cmds = _build_commands("ethernet 1/0/1", None, None, "present")
    assert cmds == ["interface ethernet 1/0/1", "ip dhcp snooping server-screen", "exit"]


def test_set_with_ip():
    cmds = _build_commands("ethernet 1/0/1", "10.0.0.1", None, "present")
    assert cmds == ["interface ethernet 1/0/1", "ip dhcp snooping server-screen 10.0.0.1", "exit"]


def test_set_with_ip_and_profile():
    cmds = _build_commands("ethernet 1/0/1", "10.0.0.1", "myprofile", "present")
    assert cmds == ["interface ethernet 1/0/1", "ip dhcp snooping server-screen 10.0.0.1 profile myprofile", "exit"]


def test_remove():
    cmds = _build_commands("ethernet 1/0/1", None, None, "absent")
    assert cmds == ["interface ethernet 1/0/1", "no ip dhcp snooping server-screen", "exit"]


def test_remove_with_ip():
    cmds = _build_commands("ethernet 1/0/1", "10.0.0.1", None, "absent")
    assert cmds == ["interface ethernet 1/0/1", "no ip dhcp snooping server-screen 10.0.0.1", "exit"]
