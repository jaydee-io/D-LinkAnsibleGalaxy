"""Unit tests for spanning_tree_priority module."""

from spanning_tree_priority import _build_commands


def test_set_priority():
    assert _build_commands(4096, "present") == ["spanning-tree priority 4096"]


def test_reset():
    assert _build_commands(None, "absent") == ["no spanning-tree priority"]
