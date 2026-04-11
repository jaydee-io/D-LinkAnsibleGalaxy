"""Unit tests for dhcp_snooping_enable module command builder."""

from dhcp_snooping_enable import _build_commands


def test_enable():
    cmds = _build_commands("enabled")
    assert cmds == ["ip dhcp snooping"]


def test_disable():
    cmds = _build_commands("disabled")
    assert cmds == ["no ip dhcp snooping"]
