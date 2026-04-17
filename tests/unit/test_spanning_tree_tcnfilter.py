"""Unit tests for spanning_tree_tcnfilter module."""

from spanning_tree_tcnfilter import _build_commands


def test_enable():
    assert _build_commands("eth1/0/7", "enabled") == [
        "interface eth1/0/7", "spanning-tree tcnfilter", "exit"]


def test_disable():
    assert _build_commands("eth1/0/7", "disabled") == [
        "interface eth1/0/7", "no spanning-tree tcnfilter", "exit"]
