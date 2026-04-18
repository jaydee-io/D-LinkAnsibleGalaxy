"""Unit tests for time_range module."""

from time_range import _build_commands


def test_create():
    assert _build_commands("rdtime", "present") == ["time-range rdtime", "exit"]


def test_delete():
    assert _build_commands("rdtime", "absent") == ["no time-range rdtime"]
