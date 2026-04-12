"""Unit tests for show_errdisable_recovery module."""

from show_errdisable_recovery import _build_command


def test_build_command():
    assert _build_command() == "show errdisable recovery"
