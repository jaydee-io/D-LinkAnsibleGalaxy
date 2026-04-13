"""Unit tests for ip_verify_source module."""

from ip_verify_source import _build_commands


def test_enable():
    assert _build_commands("eth1/0/1", False, "enabled") == [
        "interface eth1/0/1",
        "ip verify source vlan dhcp-snooping",
        "exit",
    ]


def test_enable_ip_mac():
    assert _build_commands("eth1/0/1", True, "enabled") == [
        "interface eth1/0/1",
        "ip verify source vlan dhcp-snooping ip-mac",
        "exit",
    ]


def test_disable():
    assert _build_commands("eth1/0/1", False, "disabled") == [
        "interface eth1/0/1",
        "no ip verify source vlan dhcp-snooping",
        "exit",
    ]
