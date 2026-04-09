"""Unit tests for dhcp_client_class_id module command builder."""

from dhcp_client_class_id import _build_commands


def test_set_string():
    cmds = _build_commands("vlan 100", "VOIP-Device", False, "present")
    assert cmds == ["interface vlan 100", "ip dhcp client class-id VOIP-Device", "exit"]


def test_set_hex():
    cmds = _build_commands("vlan 100", "112233", True, "present")
    assert cmds == ["interface vlan 100", "ip dhcp client class-id hex 112233", "exit"]


def test_reset():
    cmds = _build_commands("vlan 100", None, False, "absent")
    assert cmds == ["interface vlan 100", "no ip dhcp client class-id", "exit"]
