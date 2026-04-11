"""Unit tests for dhcp_relay_info_format_remote_id module command builder."""

from dhcp_relay_info_format_remote_id import _build_commands


def test_default():
    cmds = _build_commands("default", None, "present")
    assert cmds == ["ip dhcp relay information option format remote-id default"]


def test_string():
    cmds = _build_commands("string", "switch1", "present")
    assert cmds == ["ip dhcp relay information option format remote-id string switch1"]


def test_vendor2():
    cmds = _build_commands("vendor2", None, "present")
    assert cmds == ["ip dhcp relay information option format remote-id vendor2"]


def test_remove():
    cmds = _build_commands(None, None, "absent")
    assert cmds == ["no ip dhcp relay information option format remote-id"]
