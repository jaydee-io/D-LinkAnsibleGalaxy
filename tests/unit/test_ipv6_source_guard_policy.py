"""Unit tests for ipv6_source_guard_policy module."""

from ipv6_source_guard_policy import _build_commands


def test_present():
    assert _build_commands("policy1", "present") == [
        "ipv6 source-guard policy policy1"
    ]


def test_absent():
    assert _build_commands("policy1", "absent") == [
        "no ipv6 source-guard policy policy1"
    ]
