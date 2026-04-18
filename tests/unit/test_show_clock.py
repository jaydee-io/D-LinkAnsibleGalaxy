"""Unit tests for show_clock module."""

from show_clock import _build_command


def test_build():
    assert _build_command() == "show clock"
