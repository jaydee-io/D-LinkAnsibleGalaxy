"""Unit tests for nd_inspection_policy module command builder."""

from nd_inspection_policy import _build_commands


def test_create_policy():
    assert _build_commands("policy1", "present") == ["ipv6 nd inspection policy policy1"]


def test_remove_policy():
    assert _build_commands("policy1", "absent") == ["no ipv6 nd inspection policy policy1"]
