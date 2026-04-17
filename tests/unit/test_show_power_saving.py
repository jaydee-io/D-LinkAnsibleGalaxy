"""Unit tests for show_power_saving module command builder."""

from show_power_saving import _build_command


def test_default():
    assert _build_command(None) == "show power-saving"


def test_single():
    assert _build_command(["link-detection"]) == "show power-saving link-detection"


def test_multiple():
    assert _build_command(["link-detection", "eee"]) == "show power-saving link-detection eee"
