"""Unit tests for mgmt_terminal_width module command builder."""

from mgmt_terminal_width import _build_commands


def test_set_width():
    assert _build_commands(132, False) == ["terminal width 132"]


def test_set_default_width():
    assert _build_commands(80, True) == ["terminal width default 80"]
