"""Unit tests for ipv6_snooping_limit_address_count module."""

from ipv6_snooping_limit_address_count import _build_commands


def test_present():
    assert _build_commands("policy1", 25, "present") == [
        "ipv6 snooping policy policy1",
        "limit address-count 25",
        "exit",
    ]


def test_absent():
    assert _build_commands("policy1", None, "absent") == [
        "ipv6 snooping policy policy1",
        "no limit address-count",
        "exit",
    ]
