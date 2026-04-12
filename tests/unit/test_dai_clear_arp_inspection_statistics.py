"""Unit tests for dai_clear_arp_inspection_statistics module command builder."""

from dai_clear_arp_inspection_statistics import _build_commands


def test_clear_all():
    cmds = _build_commands(None)
    assert cmds == ["clear ip arp inspection statistics all"]


def test_clear_vlan():
    cmds = _build_commands("1")
    assert cmds == ["clear ip arp inspection statistics vlan 1"]
