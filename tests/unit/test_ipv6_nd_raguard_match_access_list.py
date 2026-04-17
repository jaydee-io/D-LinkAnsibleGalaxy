"""Unit tests for ipv6_nd_raguard_match_access_list module command builder."""

from ipv6_nd_raguard_match_access_list import _build_commands


def test_set_access_list():
    assert _build_commands("raguard1", "list1", "present") == [
        "ipv6 nd raguard policy raguard1",
        "match ipv6 access-list list1",
        "exit",
    ]


def test_remove_access_list():
    assert _build_commands("raguard1", None, "absent") == [
        "ipv6 nd raguard policy raguard1",
        "no match ipv6 access-list",
        "exit",
    ]
