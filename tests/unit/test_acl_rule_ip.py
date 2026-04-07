"""Unit tests for acl_rule_ip module command builder."""

from acl_rule_ip import _build_commands


def test_add_rule_extended():
    cmds = _build_commands("Strict-Control", True, "permit tcp any 10.20.0.0 0.0.255.255", None, "present")
    assert cmds == [
        "ip access-list extended Strict-Control",
        "permit tcp any 10.20.0.0 0.0.255.255",
        "exit",
    ]


def test_add_rule_standard():
    cmds = _build_commands("std-acl", False, "permit any 10.20.0.0 0.0.255.255", None, "present")
    assert cmds == [
        "ip access-list std-acl",
        "permit any 10.20.0.0 0.0.255.255",
        "exit",
    ]


def test_add_rule_with_sequence():
    cmds = _build_commands("Strict-Control", True, "5 permit tcp any 10.30.0.0 0.0.255.255", None, "present")
    assert cmds == [
        "ip access-list extended Strict-Control",
        "5 permit tcp any 10.30.0.0 0.0.255.255",
        "exit",
    ]


def test_remove_rule():
    cmds = _build_commands("Strict-Control", True, None, 10, "absent")
    assert cmds == [
        "ip access-list extended Strict-Control",
        "no 10",
        "exit",
    ]
