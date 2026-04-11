"""Unit tests for dhcp_snooping_server_screen_log_buffer module command builder."""

from dhcp_snooping_server_screen_log_buffer import _build_commands


def test_set():
    cmds = _build_commands(128, "present")
    assert cmds == ["ip dhcp snooping server-screen log-buffer entries 128"]


def test_remove():
    cmds = _build_commands(None, "absent")
    assert cmds == ["no ip dhcp snooping server-screen log-buffer entries"]
