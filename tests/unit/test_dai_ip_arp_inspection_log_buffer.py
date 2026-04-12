"""Unit tests for dai_ip_arp_inspection_log_buffer module command builder."""

from dai_ip_arp_inspection_log_buffer import _build_commands


def test_set():
    cmds = _build_commands(64, "present")
    assert cmds == ["ip arp inspection log-buffer entries 64"]


def test_remove():
    cmds = _build_commands(None, "absent")
    assert cmds == ["no ip arp inspection log-buffer entries"]
