"""Unit tests for policy_map module command builder."""

from policy_map import _build_commands


def test_create():
    assert _build_commands("policy1", "present") == [
        "policy-map policy1",
        "exit",
    ]


def test_delete():
    assert _build_commands("policy1", "absent") == [
        "no policy-map policy1",
    ]
