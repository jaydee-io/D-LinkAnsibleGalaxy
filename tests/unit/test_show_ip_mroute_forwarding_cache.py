"""Unit tests for show_ip_mroute_forwarding_cache module."""

from show_ip_mroute_forwarding_cache import _build_command


def test_no_params():
    assert _build_command(None, None) == "show ip mroute forwarding-cache"


def test_group():
    assert _build_command("239.0.0.0", None) == (
        "show ip mroute forwarding-cache group-addr 239.0.0.0"
    )


def test_group_and_source():
    assert _build_command("239.0.0.0", "10.1.1.1") == (
        "show ip mroute forwarding-cache group-addr 239.0.0.0 source-addr 10.1.1.1"
    )
