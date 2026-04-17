"""Unit tests for dim_led module command builder."""

from dim_led import _build_commands


def test_enable():
    assert _build_commands("enabled") == ["dim led"]


def test_disable():
    assert _build_commands("disabled") == ["no dim led"]
