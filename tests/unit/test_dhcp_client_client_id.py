"""Unit tests for dhcp_client_client_id module command builder."""

from dhcp_client_client_id import _build_commands


def test_set_client_id():
    cmds = _build_commands("vlan 100", "vlan 100", "present")
    assert cmds == ["interface vlan 100", "ip dhcp client client-id vlan 100", "exit"]


def test_reset_client_id():
    cmds = _build_commands("vlan 100", None, "absent")
    assert cmds == ["interface vlan 100", "no ip dhcp client client-id", "exit"]
