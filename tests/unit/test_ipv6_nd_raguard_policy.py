"""Unit tests for ipv6_nd_raguard_policy module command builder."""

from ipv6_nd_raguard_policy import _build_commands


def test_create_policy():
    assert _build_commands("policy1", "present") == [
        "ipv6 nd raguard policy policy1",
        "exit",
    ]


def test_remove_policy():
    assert _build_commands("policy1", "absent") == [
        "no ipv6 nd raguard policy policy1",
    ]
