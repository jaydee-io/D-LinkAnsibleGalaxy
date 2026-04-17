"""Unit tests for rmon_collection_history module command builder."""

from rmon_collection_history import _build_commands


def test_full():
    assert _build_commands("eth1/0/8", 101, "it@domain.com", None, 2000, "present") == [
        "interface eth1/0/8",
        "rmon collection history 101 owner it@domain.com interval 2000",
        "exit",
    ]


def test_with_buckets():
    assert _build_commands("eth1/0/1", 1, None, 100, 30, "present") == [
        "interface eth1/0/1",
        "rmon collection history 1 buckets 100 interval 30",
        "exit",
    ]


def test_minimal():
    assert _build_commands("eth1/0/1", 1, None, None, None, "present") == [
        "interface eth1/0/1",
        "rmon collection history 1",
        "exit",
    ]


def test_disable():
    assert _build_commands("eth1/0/8", 101, None, None, None, "absent") == [
        "interface eth1/0/8",
        "no rmon collection history 101",
        "exit",
    ]
