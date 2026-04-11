"""Unit tests for dhcpv6_relay_remote_id_profile module command builder."""

from dhcpv6_relay_remote_id_profile import _build_commands


def test_create():
    cmds = _build_commands("profile1", "present")
    assert cmds == ["ipv6 dhcp relay remote-id profile profile1"]


def test_remove():
    cmds = _build_commands("profile1", "absent")
    assert cmds == ["no ipv6 dhcp relay remote-id profile profile1"]
