"""Unit tests for show_logging module."""

from show_logging import _build_command


def test_default():
    assert _build_command(False) == "show logging"


def test_all():
    assert _build_command(True) == "show logging all"
