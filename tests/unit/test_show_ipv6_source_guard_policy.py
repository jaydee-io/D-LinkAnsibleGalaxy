"""Unit tests for show_ipv6_source_guard_policy module."""

from show_ipv6_source_guard_policy import _build_command


def test_no_params():
    assert _build_command(None) == "show ipv6 source-guard policy"


def test_policy():
    assert _build_command("policy1") == "show ipv6 source-guard policy policy1"
