"""Unit tests for ipv6_source_guard_deny_global_autoconfig module."""

from ipv6_source_guard_deny_global_autoconfig import _build_commands


def test_enabled():
    assert _build_commands("policy1", "enabled") == [
        "ipv6 source-guard policy policy1",
        "deny global-autoconfig",
        "exit",
    ]


def test_disabled():
    assert _build_commands("policy1", "disabled") == [
        "ipv6 source-guard policy policy1",
        "no deny global-autoconfig",
        "exit",
    ]
