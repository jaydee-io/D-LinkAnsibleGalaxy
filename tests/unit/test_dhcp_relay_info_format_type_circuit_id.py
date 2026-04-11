"""Unit tests for dhcp_relay_info_format_type_circuit_id module command builder."""

from dhcp_relay_info_format_type_circuit_id import _build_commands


def test_set():
    cmds = _build_commands("eth1/0/1", "abc", "present")
    assert cmds == ["interface eth1/0/1", "ip dhcp relay information option format-type circuit-id vendor3 string abc", "exit"]


def test_remove():
    cmds = _build_commands("eth1/0/1", None, "absent")
    assert cmds == ["interface eth1/0/1", "no ip dhcp relay information option format-type circuit-id vendor3 string", "exit"]
