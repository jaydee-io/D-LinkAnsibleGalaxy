"""Unit tests for spanning_tree_port_priority module."""

from spanning_tree_port_priority import _build_commands


def test_set_priority():
    assert _build_commands("eth1/0/7", 0, "present") == [
        "interface eth1/0/7", "spanning-tree port-priority 0", "exit"]


def test_reset():
    assert _build_commands("eth1/0/7", None, "absent") == [
        "interface eth1/0/7", "no spanning-tree port-priority", "exit"]
