"""Unit tests for dhcp_snooping_station_move_deny module command builder."""

from dhcp_snooping_station_move_deny import _build_commands


def test_enable():
    cmds = _build_commands("enabled")
    assert cmds == ["ip dhcp snooping station-move deny"]


def test_disable():
    cmds = _build_commands("disabled")
    assert cmds == ["no ip dhcp snooping station-move deny"]
