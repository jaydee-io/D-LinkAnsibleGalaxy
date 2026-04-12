"""Unit tests for dai_ip_arp_inspection_trust module command builder."""

from dai_ip_arp_inspection_trust import _build_commands


def test_trust():
    cmds = _build_commands("eth1/0/3", "enabled")
    assert cmds == ["interface eth1/0/3", "ip arp inspection trust", "exit"]


def test_untrust():
    cmds = _build_commands("eth1/0/3", "disabled")
    assert cmds == ["interface eth1/0/3", "no ip arp inspection trust", "exit"]
