"""Unit tests for dhcp_snooping_trust module command builder."""

from dhcp_snooping_trust import _build_commands


def test_enable():
    cmds = _build_commands("ethernet 1/0/1", "enabled")
    assert cmds == ["interface ethernet 1/0/1", "ip dhcp snooping trust"]


def test_disable():
    cmds = _build_commands("ethernet 1/0/1", "disabled")
    assert cmds == ["interface ethernet 1/0/1", "no ip dhcp snooping trust"]
