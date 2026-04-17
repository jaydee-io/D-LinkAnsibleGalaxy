"""Unit tests for ipv6_nd_raguard_attach_policy module command builder."""

from ipv6_nd_raguard_attach_policy import _build_commands


def test_attach_policy():
    assert _build_commands("eth1/0/3", "raguard1", "present") == [
        "interface eth1/0/3",
        "ipv6 nd raguard attach-policy raguard1",
        "exit",
    ]


def test_attach_default():
    assert _build_commands("eth1/0/3", None, "present") == [
        "interface eth1/0/3",
        "ipv6 nd raguard attach-policy",
        "exit",
    ]


def test_remove():
    assert _build_commands("eth1/0/3", None, "absent") == [
        "interface eth1/0/3",
        "no ipv6 nd raguard",
        "exit",
    ]
