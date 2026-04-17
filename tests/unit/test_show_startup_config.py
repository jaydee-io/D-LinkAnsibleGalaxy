"""Unit tests for show_startup_config module."""

from show_startup_config import _build_command


def test_build():
    assert _build_command() == "show startup-config"
