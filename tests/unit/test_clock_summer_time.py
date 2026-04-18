"""Unit tests for clock_summer_time module."""

from clock_summer_time import _build_commands


def test_recurring():
    assert _build_commands("recurring", "1 sun jun 2:00", "last sun oct 2:00", None, "present") == [
        "clock summer-time recurring 1 sun jun 2:00 last sun oct 2:00"]


def test_recurring_with_offset():
    assert _build_commands("recurring", "1 sun jun 2:00", "last sun oct 2:00", 90, "present") == [
        "clock summer-time recurring 1 sun jun 2:00 last sun oct 2:00 90"]


def test_date():
    assert _build_commands("date", "1 jun 2023 2:00", "31 oct 2023 2:00", None, "present") == [
        "clock summer-time date 1 jun 2023 2:00 31 oct 2023 2:00"]


def test_absent():
    assert _build_commands(None, None, None, None, "absent") == ["no clock summer-time"]
