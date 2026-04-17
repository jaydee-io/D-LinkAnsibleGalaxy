"""Unit tests for show_boot module."""

from show_boot import _build_command


def test_build():
    assert _build_command() == "show boot"
