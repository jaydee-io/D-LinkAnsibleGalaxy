"""Unit tests for mld_snooping_query_max_response_time module."""

from mld_snooping_query_max_response_time import _build_commands


def test_set():
    assert _build_commands(1000, 20, "present") == [
        "vlan 1000", "ipv6 mld snooping query-max-response-time 20", "exit"]


def test_reset():
    assert _build_commands(1000, None, "absent") == [
        "vlan 1000", "no ipv6 mld snooping query-max-response-time", "exit"]
