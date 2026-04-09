"""Unit tests for aaa_ip_tacacs_source_interface module command builder."""

from aaa_ip_tacacs_source_interface import _build_commands


def test_present():
    cmds = _build_commands("vlan100", "present")
    assert cmds == ["ip tacacs source-interface vlan100"]


def test_absent():
    cmds = _build_commands(None, "absent")
    assert cmds == ["no ip tacacs source-interface"]
