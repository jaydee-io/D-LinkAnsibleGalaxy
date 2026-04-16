"""Unit tests for nd_inspection_validate_source_mac module command builder."""

from nd_inspection_validate_source_mac import _build_commands


def test_enable():
    assert _build_commands("policy1", "enabled") == [
        "ipv6 nd inspection policy policy1",
        "validate source-mac",
        "exit",
    ]


def test_disable():
    assert _build_commands("policy1", "disabled") == [
        "ipv6 nd inspection policy policy1",
        "no validate source-mac",
        "exit",
    ]
