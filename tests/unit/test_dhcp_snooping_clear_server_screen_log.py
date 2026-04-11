"""Unit tests for dhcp_snooping_clear_server_screen_log module command builder."""

from dhcp_snooping_clear_server_screen_log import _build_commands


def test_clear():
    cmds = _build_commands()
    assert cmds == ["clear ip dhcp snooping server-screen log"]
