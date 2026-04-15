"""Unit tests for show_lldp module."""

from show_lldp import _build_command


def test_command():
    assert _build_command() == "show lldp"
