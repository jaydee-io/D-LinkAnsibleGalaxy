"""Unit tests for ipv6_source_guard_attach_policy module."""

from ipv6_source_guard_attach_policy import _build_commands


def test_present_with_policy():
    assert _build_commands("eth1/0/3", "pol1", "present") == [
        "interface eth1/0/3",
        "ipv6 source-guard attach-policy pol1",
        "exit",
    ]


def test_present_default():
    assert _build_commands("eth1/0/3", None, "present") == [
        "interface eth1/0/3",
        "ipv6 source-guard attach-policy",
        "exit",
    ]


def test_absent():
    assert _build_commands("eth1/0/3", None, "absent") == [
        "interface eth1/0/3",
        "no ipv6 source-guard attach-policy",
        "exit",
    ]
