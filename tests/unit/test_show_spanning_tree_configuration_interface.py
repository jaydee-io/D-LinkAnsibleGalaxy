"""Unit tests for show_spanning_tree_configuration_interface module."""

from show_spanning_tree_configuration_interface import _build_command


def test_no_params():
    assert _build_command(None) == "show spanning-tree configuration interface"


def test_with_interface():
    assert _build_command("eth1/0/1") == "show spanning-tree configuration interface eth1/0/1"
