"""Unit tests for dhcpv6_relay_remote_id_udf module command builder."""

from dhcpv6_relay_remote_id_udf import _build_commands


def test_set_ascii():
    cmds = _build_commands("PARADISE001", False, "present")
    assert cmds == ["ipv6 dhcp relay remote-id udf ascii PARADISE001"]


def test_set_hex():
    cmds = _build_commands("010c08", True, "present")
    assert cmds == ["ipv6 dhcp relay remote-id udf hex 010c08"]


def test_remove():
    cmds = _build_commands(None, False, "absent")
    assert cmds == ["no ipv6 dhcp relay remote-id udf"]
