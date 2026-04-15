"""Unit tests for show_lldp_interface module."""

from show_lldp_interface import _build_command


def test_command():
    assert _build_command("eth1/0/1") == "show lldp interface eth1/0/1"
