"""Unit tests for mgmt_terminal_length module command builder."""

from mgmt_terminal_length import _build_commands


def test_set_length():
    assert _build_commands(24, False) == ["terminal length 24"]


def test_set_default_length():
    assert _build_commands(48, True) == ["terminal length default 48"]


def test_set_zero():
    assert _build_commands(0, False) == ["terminal length 0"]
