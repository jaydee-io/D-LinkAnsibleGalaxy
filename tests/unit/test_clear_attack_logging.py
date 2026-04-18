"""Unit tests for clear_attack_logging module."""

from clear_attack_logging import _build_commands


def test_build():
    assert _build_commands() == ["clear attack-logging"]
