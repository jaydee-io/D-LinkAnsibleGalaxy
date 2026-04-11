"""Unit tests for dhcp_relay_info_format_circuit_id module command builder."""

from dhcp_relay_info_format_circuit_id import _build_commands


def test_vendor1():
    cmds = _build_commands("vendor1", None, "present")
    assert cmds == ["ip dhcp relay information option format circuit-id vendor1"]


def test_string():
    cmds = _build_commands("string", "abcd", "present")
    assert cmds == ["ip dhcp relay information option format circuit-id string abcd"]


def test_remove():
    cmds = _build_commands(None, None, "absent")
    assert cmds == ["no ip dhcp relay information option format circuit-id"]
