"""Unit tests for policy_map_set module command builder."""

from policy_map_set import _build_commands


def test_set_ip_dscp():
    assert _build_commands("policy1", "class1", "ip-dscp", 10, "present") == [
        "policy-map policy1",
        "class class1",
        "set ip dscp 10",
        "exit",
        "exit",
    ]


def test_set_cos():
    assert _build_commands("p", "c", "cos", 5, "present") == [
        "policy-map p",
        "class c",
        "set cos 5",
        "exit",
        "exit",
    ]


def test_remove():
    assert _build_commands("p", "c", "ip-dscp", 10, "absent") == [
        "policy-map p",
        "class c",
        "no set ip dscp 10",
        "exit",
        "exit",
    ]
