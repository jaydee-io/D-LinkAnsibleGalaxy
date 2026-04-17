"""Unit tests for spanning_tree_forward_bpdu module."""

from spanning_tree_forward_bpdu import _build_commands


def test_enable():
    assert _build_commands("eth1/0/2", "enabled") == [
        "interface eth1/0/2", "spanning-tree forward-bpdu", "exit"]


def test_disable():
    assert _build_commands("eth1/0/2", "disabled") == [
        "interface eth1/0/2", "no spanning-tree forward-bpdu", "exit"]
