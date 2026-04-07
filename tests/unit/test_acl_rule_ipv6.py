"""Unit tests for acl_rule_ipv6 module command builder."""

from acl_rule_ipv6 import _build_commands


def test_add_rule_extended():
    cmds = _build_commands("ipv6-control", True, "permit tcp any ff02::0:2/16", None, "present")
    assert cmds == [
        "ipv6 access-list extended ipv6-control",
        "permit tcp any ff02::0:2/16",
        "exit",
    ]


def test_add_rule_standard():
    cmds = _build_commands("ipv6-std-control", False, "permit any fe80::101:1/54", None, "present")
    assert cmds == [
        "ipv6 access-list ipv6-std-control",
        "permit any fe80::101:1/54",
        "exit",
    ]


def test_remove_rule():
    cmds = _build_commands("ipv6-control", True, None, 10, "absent")
    assert cmds == [
        "ipv6 access-list extended ipv6-control",
        "no 10",
        "exit",
    ]
