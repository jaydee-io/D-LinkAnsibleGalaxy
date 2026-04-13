"""Unit tests for show_ipv6_mroute_forwarding_cache module."""

from show_ipv6_mroute_forwarding_cache import _build_command


def test_no_params():
    assert _build_command(None, None) == "show ipv6 mroute forwarding-cache"


def test_group():
    assert _build_command("FF0E::1:1:1", None) == (
        "show ipv6 mroute forwarding-cache group-addr FF0E::1:1:1"
    )


def test_group_and_source():
    assert _build_command("FF0E::1:1:1", "2000:60:1:1::10") == (
        "show ipv6 mroute forwarding-cache group-addr FF0E::1:1:1 source-addr 2000:60:1:1::10"
    )
