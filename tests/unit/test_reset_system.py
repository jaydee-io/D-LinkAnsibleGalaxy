"""Unit tests for reset_system module."""

from reset_system import _build_commands


def test_build():
    assert _build_commands() == ["reset system"]
