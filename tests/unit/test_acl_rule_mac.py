"""Unit tests for acl_rule_mac module command builder."""

from acl_rule_mac import _build_commands


def test_add_rule():
    cmds = _build_commands("daily-profile", "permit 00:80:33:00:00:00 00:00:00:ff:ff:ff any", None, "present")
    assert cmds == [
        "mac access-list extended daily-profile",
        "permit 00:80:33:00:00:00 00:00:00:ff:ff:ff any",
        "exit",
    ]


def test_add_rule_with_ethernet_type():
    cmds = _build_commands("daily-profile", "deny any any ethernet-type arp FFFF", None, "present")
    assert cmds == [
        "mac access-list extended daily-profile",
        "deny any any ethernet-type arp FFFF",
        "exit",
    ]


def test_remove_rule():
    cmds = _build_commands("daily-profile", None, 10, "absent")
    assert cmds == [
        "mac access-list extended daily-profile",
        "no 10",
        "exit",
    ]
