"""Unit tests for policy_map_class module command builder."""

from policy_map_class import _build_commands


def test_attach_class():
    assert _build_commands("policy1", "class-dscp-red", "present") == [
        "policy-map policy1",
        "class class-dscp-red",
        "exit",
        "exit",
    ]


def test_remove_class():
    assert _build_commands("policy", "class1", "absent") == [
        "policy-map policy",
        "no class class1",
        "exit",
    ]


def test_class_default():
    assert _build_commands("policy1", "class-default", "present") == [
        "policy-map policy1",
        "class class-default",
        "exit",
        "exit",
    ]
