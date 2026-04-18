"""Unit tests for clear_logging module."""

from clear_logging import _build_commands


def test_build():
    assert _build_commands() == ["clear logging"]
