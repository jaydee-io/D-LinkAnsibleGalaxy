"""Unit tests for clear_spanning_tree_detected_protocols module."""

from clear_spanning_tree_detected_protocols import _build_commands


def test_all():
    assert _build_commands("all", None) == [
        "clear spanning-tree detected-protocols all"]


def test_interface():
    assert _build_commands("interface", "eth1/0/1") == [
        "clear spanning-tree detected-protocols interface eth1/0/1"]
