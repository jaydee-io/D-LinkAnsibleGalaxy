"""Unit tests for spanning_tree_cost module."""

from spanning_tree_cost import _build_commands


def test_set_cost():
    assert _build_commands("eth1/0/7", 20000, "present") == [
        "interface eth1/0/7", "spanning-tree cost 20000", "exit"]


def test_reset_cost():
    assert _build_commands("eth1/0/7", None, "absent") == [
        "interface eth1/0/7", "no spanning-tree cost", "exit"]
