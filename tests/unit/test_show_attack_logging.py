"""Unit tests for show_attack_logging module."""

from show_attack_logging import _build_command


def test_default():
    assert _build_command(None) == "show attack-logging"


def test_with_index():
    assert _build_command(1) == "show attack-logging index 1"
