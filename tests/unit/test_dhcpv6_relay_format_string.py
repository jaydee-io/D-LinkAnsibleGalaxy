"""Unit tests for dhcpv6_relay_format_string module command builder."""

from dhcpv6_relay_format_string import _build_commands


def test_set():
    cmds = _build_commands("profile1", "%port:%sysname:%05svlan", "present")
    assert cmds == ["ipv6 dhcp relay remote-id profile profile1", "format string %port:%sysname:%05svlan", "exit"]


def test_remove():
    cmds = _build_commands("profile1", None, "absent")
    assert cmds == ["ipv6 dhcp relay remote-id profile profile1", "no format string", "exit"]
