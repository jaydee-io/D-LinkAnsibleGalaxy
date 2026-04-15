"""Unit tests for show_lldp_traffic module."""

from show_lldp_traffic import _build_command


def test_command():
    assert _build_command() == "show lldp traffic"
