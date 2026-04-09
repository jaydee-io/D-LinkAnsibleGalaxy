"""Unit tests for debug_copy module command builder."""

from debug_copy import _build_commands


def test_copy_tech_support():
    cmds = _build_commands("tech-support", "tftp://10.90.90.99/abc.txt")
    assert cmds == ["debug copy tech-support tftp://10.90.90.99/abc.txt"]


def test_copy_error_log():
    cmds = _build_commands("error-log", "tftp://10.90.90.99/error.txt")
    assert cmds == ["debug copy error-log tftp://10.90.90.99/error.txt"]
