"""Unit tests for mgmt_clear_line module command builder."""

from mgmt_clear_line import _build_commands


def test_clear_line():
    assert _build_commands(2) == ["clear line 2"]


def test_clear_line_1():
    assert _build_commands(1) == ["clear line 1"]
