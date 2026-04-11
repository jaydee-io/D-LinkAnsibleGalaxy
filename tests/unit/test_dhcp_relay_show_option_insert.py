"""Unit tests for dhcp_relay_show_option_insert module command builder."""

from dhcp_relay_show_option_insert import _build_command


def test_build_command():
    cmd = _build_command()
    assert cmd == "show ip dhcp relay information option-insert"
