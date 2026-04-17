"""Unit tests for queue_rate_limit module command builder."""

from queue_rate_limit import _build_commands


def test_kbps():
    assert _build_commands("eth1/0/1", 1, 100, 2000, None, None, "present") == [
        "interface eth1/0/1",
        "queue 1 rate-limit 100 2000",
        "exit",
    ]


def test_percent():
    assert _build_commands("eth1/0/1", 2, None, None, 10, 50, "present") == [
        "interface eth1/0/1",
        "queue 2 rate-limit percent 10 percent 50",
        "exit",
    ]


def test_mixed():
    assert _build_commands("eth1/0/1", 3, 100, None, None, 50, "present") == [
        "interface eth1/0/1",
        "queue 3 rate-limit 100 percent 50",
        "exit",
    ]


def test_remove():
    assert _build_commands("eth1/0/1", 1, None, None, None, None, "absent") == [
        "interface eth1/0/1",
        "no queue 1 rate-limit",
        "exit",
    ]
