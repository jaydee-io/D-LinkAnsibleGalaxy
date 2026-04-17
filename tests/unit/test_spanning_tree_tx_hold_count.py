"""Unit tests for spanning_tree_tx_hold_count module."""

from spanning_tree_tx_hold_count import _build_commands


def test_set_value():
    assert _build_commands(5, "present") == ["spanning-tree tx-hold-count 5"]


def test_reset():
    assert _build_commands(None, "absent") == ["no spanning-tree tx-hold-count"]
