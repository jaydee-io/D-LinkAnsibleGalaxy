"""Unit tests for debug_show_tech_support module command builder."""

from debug_show_tech_support import _build_command


def test_build_command():
    cmd = _build_command()
    assert cmd == "debug show tech-support"
