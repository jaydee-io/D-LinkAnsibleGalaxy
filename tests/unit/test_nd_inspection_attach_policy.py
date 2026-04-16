"""Unit tests for nd_inspection_attach_policy module command builder."""

from nd_inspection_attach_policy import _build_commands


def test_attach_named_policy():
    assert _build_commands("eth1/0/3", "policy1", "present") == [
        "interface eth1/0/3",
        "ipv6 nd inspection attach-policy policy1",
        "exit",
    ]


def test_attach_default_policy():
    assert _build_commands("eth1/0/3", None, "present") == [
        "interface eth1/0/3",
        "ipv6 nd inspection attach-policy",
        "exit",
    ]


def test_detach_policy():
    assert _build_commands("eth1/0/3", None, "absent") == [
        "interface eth1/0/3",
        "no ipv6 nd inspection attach-policy",
        "exit",
    ]
