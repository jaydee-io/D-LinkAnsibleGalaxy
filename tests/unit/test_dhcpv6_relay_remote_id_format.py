"""Unit tests for dhcpv6_relay_remote_id_format module command builder."""

from dhcpv6_relay_remote_id_format import _build_commands


def test_set_cid():
    cmds = _build_commands("cid-with-user-define", "present")
    assert cmds == ["ipv6 dhcp relay remote-id format cid-with-user-define"]


def test_set_default():
    cmds = _build_commands("default", "present")
    assert cmds == ["ipv6 dhcp relay remote-id format default"]


def test_reset():
    cmds = _build_commands(None, "absent")
    assert cmds == ["no ipv6 dhcp relay remote-id format"]
