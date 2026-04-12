"""Unit tests for dai_ip_arp_inspection_validate module command builder."""

from dai_ip_arp_inspection_validate import _build_commands


def test_enable_src_mac():
    cmds = _build_commands(True, False, False, "present")
    assert cmds == ["ip arp inspection validate src-mac"]


def test_enable_all():
    cmds = _build_commands(True, True, True, "present")
    assert cmds == ["ip arp inspection validate src-mac dst-mac ip"]


def test_enable_none():
    cmds = _build_commands(False, False, False, "present")
    assert cmds == ["ip arp inspection validate"]


def test_remove_src_mac():
    cmds = _build_commands(True, False, False, "absent")
    assert cmds == ["no ip arp inspection validate src-mac"]
