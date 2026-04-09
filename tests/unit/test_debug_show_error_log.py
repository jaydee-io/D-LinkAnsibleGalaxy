"""Unit tests for debug_show_error_log module command builder."""

from debug_show_error_log import _build_command


def test_build_command():
    cmd = _build_command()
    assert cmd == "debug show error-log"
