"""Unit tests for dhcp_relay_info_policy_action module command builder."""

from dhcp_relay_info_policy_action import _build_commands


def test_set_drop():
    cmds = _build_commands("vlan 100", "drop", "present")
    assert cmds == ["interface vlan 100", "ip dhcp relay information policy-action drop", "exit"]


def test_remove():
    cmds = _build_commands("vlan 100", None, "absent")
    assert cmds == ["interface vlan 100", "no ip dhcp relay information policy-action", "exit"]
