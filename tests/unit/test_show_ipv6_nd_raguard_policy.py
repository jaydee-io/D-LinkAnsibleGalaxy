"""Unit tests for show_ipv6_nd_raguard_policy module command builder."""

from show_ipv6_nd_raguard_policy import _build_command


def test_show_all():
    assert _build_command(None) == "show ipv6 nd raguard policy"


def test_show_specific():
    assert _build_command("raguard1") == "show ipv6 nd raguard policy raguard1"
