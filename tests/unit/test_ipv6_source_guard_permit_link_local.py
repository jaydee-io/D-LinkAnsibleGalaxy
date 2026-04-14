"""Unit tests for ipv6_source_guard_permit_link_local module."""

from ipv6_source_guard_permit_link_local import _build_commands


def test_enabled():
    assert _build_commands("policy1", "enabled") == [
        "ipv6 source-guard policy policy1",
        "permit link-local",
        "exit",
    ]


def test_disabled():
    assert _build_commands("policy1", "disabled") == [
        "ipv6 source-guard policy policy1",
        "no permit link-local",
        "exit",
    ]
