"""Unit tests for dai_arp_access_list module command builder."""

from dai_arp_access_list import _build_commands


def test_create():
    cmds = _build_commands("static-arp-list", "present")
    assert cmds == ["arp access-list static-arp-list"]


def test_remove():
    cmds = _build_commands("static-arp-list", "absent")
    assert cmds == ["no arp access-list static-arp-list"]
