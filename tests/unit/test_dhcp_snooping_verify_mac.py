"""Unit tests for dhcp_snooping_verify_mac module command builder."""

from dhcp_snooping_verify_mac import _build_commands


def test_enable():
    cmds = _build_commands("enabled")
    assert cmds == ["ip dhcp snooping verify mac-address"]


def test_disable():
    cmds = _build_commands("disabled")
    assert cmds == ["no ip dhcp snooping verify mac-address"]
