"""Unit tests for clock_timezone module."""

from clock_timezone import _build_commands


def test_set_hours():
    assert _build_commands("-", 8, None, "present") == ["clock timezone - 8"]


def test_set_hours_minutes():
    assert _build_commands("+", 5, 30, "present") == ["clock timezone + 5 30"]


def test_absent():
    assert _build_commands(None, None, None, "absent") == ["no clock timezone"]
