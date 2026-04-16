"""Unit tests for show_nd_inspection_policy module command builder."""

from show_nd_inspection_policy import _build_command


def test_all():
    assert _build_command(None) == "show ipv6 nd inspection policy"


def test_specific():
    assert _build_command("inspect1") == "show ipv6 nd inspection policy inspect1"
