"""Unit tests for dhcp_relay_info_policy module command builder."""

from dhcp_relay_info_policy import _build_commands


def test_set_keep():
    cmds = _build_commands("keep", "present")
    assert cmds == ["ip dhcp relay information policy keep"]


def test_remove():
    cmds = _build_commands(None, "absent")
    assert cmds == ["no ip dhcp relay information policy"]
