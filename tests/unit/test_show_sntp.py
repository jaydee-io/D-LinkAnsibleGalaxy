"""Unit tests for show_sntp module."""

from show_sntp import _build_command


def test_build():
    assert _build_command() == "show sntp"
