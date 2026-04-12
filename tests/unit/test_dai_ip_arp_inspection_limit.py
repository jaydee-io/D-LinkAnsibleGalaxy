"""Unit tests for dai_ip_arp_inspection_limit module command builder."""

from dai_ip_arp_inspection_limit import _build_commands


def test_set_rate():
    cmds = _build_commands("eth1/0/10", 30, None, False, "present")
    assert cmds == ["interface eth1/0/10", "ip arp inspection limit rate 30", "exit"]


def test_set_rate_burst():
    cmds = _build_commands("eth1/0/10", 30, 5, False, "present")
    assert cmds == ["interface eth1/0/10", "ip arp inspection limit rate 30 burst interval 5", "exit"]


def test_set_no_limit():
    cmds = _build_commands("eth1/0/10", None, None, True, "present")
    assert cmds == ["interface eth1/0/10", "ip arp inspection limit none", "exit"]


def test_remove():
    cmds = _build_commands("eth1/0/10", None, None, False, "absent")
    assert cmds == ["interface eth1/0/10", "no ip arp inspection limit", "exit"]
