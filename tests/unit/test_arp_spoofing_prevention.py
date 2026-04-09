"""Unit tests for arp_spoofing_prevention module command builder."""

from arp_spoofing_prevention import _build_commands


def test_add_entry():
    assert _build_commands("10.254.254.251", "00-00-00-11-11-11", "eth1/0/10", "present") == [
        "ip arp spoofing-prevention 10.254.254.251 00-00-00-11-11-11 interface eth1/0/10",
    ]


def test_remove_entry():
    assert _build_commands("10.254.254.251", None, "eth1/0/10", "absent") == [
        "no ip arp spoofing-prevention 10.254.254.251 interface eth1/0/10",
    ]


def test_different_ip():
    assert _build_commands("192.168.1.1", "AA-BB-CC-DD-EE-FF", "eth1/0/1", "present") == [
        "ip arp spoofing-prevention 192.168.1.1 AA-BB-CC-DD-EE-FF interface eth1/0/1",
    ]
