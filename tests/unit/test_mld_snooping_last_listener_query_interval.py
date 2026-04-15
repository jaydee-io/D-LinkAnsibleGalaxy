"""Unit tests for mld_snooping_last_listener_query_interval module."""

from mld_snooping_last_listener_query_interval import _build_commands


def test_set():
    assert _build_commands(1000, 3, "present") == [
        "vlan 1000", "ipv6 mld snooping last-listener-query-interval 3", "exit"]


def test_reset():
    assert _build_commands(1000, None, "absent") == [
        "vlan 1000", "no ipv6 mld snooping last-listener-query-interval", "exit"]
