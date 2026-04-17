"""Unit tests for spanning_tree_global_state module."""

from spanning_tree_global_state import _build_commands


def test_enable():
    assert _build_commands("enabled") == ["spanning-tree global state enable"]


def test_disable():
    assert _build_commands("disabled") == ["spanning-tree global state disable"]
