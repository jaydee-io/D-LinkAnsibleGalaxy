"""Unit tests for clear_running_config module."""

from clear_running_config import _build_commands


def test_build():
    assert _build_commands() == ["clear running-config"]
