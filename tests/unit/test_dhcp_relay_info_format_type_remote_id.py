"""Unit tests for dhcp_relay_info_format_type_remote_id module command builder."""

from dhcp_relay_info_format_type_remote_id import _build_commands


def test_set():
    cmds = _build_commands("eth1/0/3", "switch1", "present")
    assert cmds == ["interface eth1/0/3", "ip dhcp relay information option format-type remote-id vendor3 string switch1", "exit"]


def test_remove():
    cmds = _build_commands("eth1/0/3", None, "absent")
    assert cmds == ["interface eth1/0/3", "no ip dhcp relay information option format-type remote-id vendor3", "exit"]
