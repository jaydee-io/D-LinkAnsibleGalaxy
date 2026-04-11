"""Unit tests for dhcp_snooping_show_server_screen_log module command builder."""

from dhcp_snooping_show_server_screen_log import _build_command


def test_show():
    cmd = _build_command()
    assert cmd == "show ip dhcp server-screen log"
