"""Unit tests for show_ipv6_route_summary module command builder."""

from show_ipv6_route_summary import _build_command


def test_default():
    assert _build_command() == "show ipv6 route summary"
