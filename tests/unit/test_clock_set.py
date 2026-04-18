"""Unit tests for clock_set module."""

from clock_set import _build_commands


def test_build():
    assert _build_commands("18:00:00", 4, "jul", 2023) == ["clock set 18:00:00 4 jul 2023"]
