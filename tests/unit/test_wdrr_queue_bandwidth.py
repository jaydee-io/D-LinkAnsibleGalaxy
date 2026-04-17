"""Unit tests for wdrr_queue_bandwidth module command builder."""

from wdrr_queue_bandwidth import _build_commands


def test_set():
    assert _build_commands("eth1/0/1", [1, 2, 3, 4, 5, 6, 7, 8], "present") == [
        "interface eth1/0/1",
        "wdrr-queue bandwidth 1 2 3 4 5 6 7 8",
        "exit",
    ]


def test_revert():
    assert _build_commands("eth1/0/1", None, "absent") == [
        "interface eth1/0/1",
        "no wdrr-queue bandwidth",
        "exit",
    ]
