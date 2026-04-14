"""Unit tests for ipv6_snooping_policy module."""

from ipv6_snooping_policy import _build_commands


def test_present():
    assert _build_commands("policy1", "present") == [
        "ipv6 snooping policy policy1"
    ]


def test_absent():
    assert _build_commands("policy1", "absent") == [
        "no ipv6 snooping policy policy1"
    ]
