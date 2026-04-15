"""Unit tests for lldp_hold_multiplier module."""

from lldp_hold_multiplier import _build_commands


def test_set():
    assert _build_commands(3, "present") == ["lldp hold-multiplier 3"]


def test_reset():
    assert _build_commands(None, "absent") == ["no lldp hold-multiplier"]
