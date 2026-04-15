"""Unit tests for show_lldp_neighbor_interface module."""

from show_lldp_neighbor_interface import _build_command


def test_normal():
    assert _build_command("eth1/0/9", None) == "show lldp neighbors interface eth1/0/9"


def test_detail():
    assert _build_command("eth1/0/9", "detail") == "show lldp neighbors interface eth1/0/9 detail"
