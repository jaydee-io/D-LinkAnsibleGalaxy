"""Unit tests for show_poe_power_module module command builder."""

from show_poe_power_module import _build_command


def test_default():
    assert _build_command(False) == "show poe power module"


def test_detail():
    assert _build_command(True) == "show poe power module detail"
