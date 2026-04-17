"""Unit tests for spanning_tree_link_type module."""

from spanning_tree_link_type import _build_commands


def test_set_point_to_point():
    assert _build_commands("eth1/0/7", "point-to-point", "present") == [
        "interface eth1/0/7", "spanning-tree link-type point-to-point", "exit"]


def test_set_shared():
    assert _build_commands("eth1/0/7", "shared", "present") == [
        "interface eth1/0/7", "spanning-tree link-type shared", "exit"]


def test_reset():
    assert _build_commands("eth1/0/7", None, "absent") == [
        "interface eth1/0/7", "no spanning-tree link-type", "exit"]
