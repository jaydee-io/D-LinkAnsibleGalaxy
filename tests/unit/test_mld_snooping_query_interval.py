"""Unit tests for mld_snooping_query_interval module."""

from mld_snooping_query_interval import _build_commands


def test_set():
    assert _build_commands(1000, 300, "present") == [
        "vlan 1000", "ipv6 mld snooping query-interval 300", "exit"]


def test_reset():
    assert _build_commands(1000, None, "absent") == [
        "vlan 1000", "no ipv6 mld snooping query-interval", "exit"]
