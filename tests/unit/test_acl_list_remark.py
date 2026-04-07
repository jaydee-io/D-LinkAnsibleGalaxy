"""Unit tests for acl_list_remark module command builder."""

from acl_list_remark import _build_commands


def test_add_remark_ip_extended():
    cmds = _build_commands("ip_extended", "R&D", "Match packets from 10.2.2.1", "present")
    assert cmds == [
        "ip access-list extended R&D",
        "list-remark Match packets from 10.2.2.1",
        "exit",
    ]


def test_add_remark_mac():
    cmds = _build_commands("mac", "daily-profile", "Daily access profile", "present")
    assert cmds == [
        "mac access-list extended daily-profile",
        "list-remark Daily access profile",
        "exit",
    ]


def test_add_remark_ipv6():
    cmds = _build_commands("ipv6", "ip6-std", "IPv6 standard list", "present")
    assert cmds == [
        "ipv6 access-list ip6-std",
        "list-remark IPv6 standard list",
        "exit",
    ]


def test_remove_remark():
    cmds = _build_commands("ip_extended", "R&D", None, "absent")
    assert cmds == [
        "ip access-list extended R&D",
        "no list-remark",
        "exit",
    ]
