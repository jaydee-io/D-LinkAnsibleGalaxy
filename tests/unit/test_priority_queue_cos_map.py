"""Unit tests for priority_queue_cos_map module command builder."""

from priority_queue_cos_map import _build_commands


def test_assign():
    assert _build_commands(2, [3, 5, 6], "present") == [
        "priority-queue cos-map 2 3 5 6",
    ]


def test_single_cos():
    assert _build_commands(0, [1], "present") == [
        "priority-queue cos-map 0 1",
    ]


def test_revert():
    assert _build_commands(2, None, "absent") == [
        "no priority-queue cos-map",
    ]
