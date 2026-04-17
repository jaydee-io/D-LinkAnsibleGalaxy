"""Unit tests for spanning_tree_state module."""

from spanning_tree_state import _build_commands


def test_enable():
    assert _build_commands("eth1/0/1", "enabled") == [
        "interface eth1/0/1", "spanning-tree state enable", "exit"]


def test_disable():
    assert _build_commands("eth1/0/1", "disabled") == [
        "interface eth1/0/1", "spanning-tree state disable", "exit"]
