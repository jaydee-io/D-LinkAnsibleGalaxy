"""Unit tests for dhcp_snooping_limit_rate module command builder."""

from dhcp_snooping_limit_rate import _build_commands


def test_set():
    cmds = _build_commands("ethernet 1/0/1", 15, "present")
    assert cmds == ["interface ethernet 1/0/1", "ip dhcp snooping limit rate 15", "exit"]


def test_remove():
    cmds = _build_commands("ethernet 1/0/1", None, "absent")
    assert cmds == ["interface ethernet 1/0/1", "no ip dhcp snooping limit rate", "exit"]
