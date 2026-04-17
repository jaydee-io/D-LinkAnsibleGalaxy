"""Unit tests for spanning_tree_portfast module."""

from spanning_tree_portfast import _build_commands


def test_set_edge():
    assert _build_commands("eth1/0/7", "edge", "present") == [
        "interface eth1/0/7", "spanning-tree portfast edge", "exit"]


def test_set_network():
    assert _build_commands("eth1/0/7", "network", "present") == [
        "interface eth1/0/7", "spanning-tree portfast network", "exit"]


def test_set_disable():
    assert _build_commands("eth1/0/7", "disable", "present") == [
        "interface eth1/0/7", "spanning-tree portfast disable", "exit"]


def test_reset():
    assert _build_commands("eth1/0/7", None, "absent") == [
        "interface eth1/0/7", "no spanning-tree portfast", "exit"]
