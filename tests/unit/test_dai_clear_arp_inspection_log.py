"""Unit tests for dai_clear_arp_inspection_log module command builder."""

from dai_clear_arp_inspection_log import _build_commands


def test_build_commands():
    cmds = _build_commands()
    assert cmds == ["clear ip arp inspection log"]
