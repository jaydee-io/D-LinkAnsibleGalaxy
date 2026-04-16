"""Unit tests for show_spanning_tree_mst module command builder."""

from show_spanning_tree_mst import _build_command


def test_default():
    assert _build_command(False, False, None, None, False) == "show spanning-tree mst"


def test_configuration():
    assert _build_command(True, False, None, None, False) == "show spanning-tree mst configuration"


def test_configuration_digest():
    assert _build_command(True, True, None, None, False) == "show spanning-tree mst configuration digest"


def test_instance_interface():
    assert _build_command(False, False, "2", "eth1/0/3-4", False) == \
        "show spanning-tree mst instance 2 interface eth1/0/3-4"


def test_detail():
    assert _build_command(False, False, None, None, True) == "show spanning-tree mst detail"
