"""Unit tests for rmon_collection_stats module command builder."""

from rmon_collection_stats import _build_commands


def test_enable_with_owner():
    assert _build_commands("eth1/0/2", 65, "guest", "present") == [
        "interface eth1/0/2",
        "rmon collection stats 65 owner guest",
        "exit",
    ]


def test_enable_no_owner():
    assert _build_commands("eth1/0/2", 65, None, "present") == [
        "interface eth1/0/2",
        "rmon collection stats 65",
        "exit",
    ]


def test_disable():
    assert _build_commands("eth1/0/2", 65, None, "absent") == [
        "interface eth1/0/2",
        "no rmon collection stats 65",
        "exit",
    ]
