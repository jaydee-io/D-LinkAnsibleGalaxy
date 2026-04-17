"""Unit tests for power_saving_hibernation_time_range module command builder."""

from power_saving_hibernation_time_range import _build_commands


def test_add():
    assert _build_commands("off-duty", "present") == ["power-saving hibernation time-range off-duty"]


def test_remove():
    assert _build_commands("off-duty", "absent") == ["no power-saving hibernation time-range off-duty"]
