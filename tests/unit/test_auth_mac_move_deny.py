"""Unit tests for auth_mac_move_deny module command builder."""

from auth_mac_move_deny import _build_commands


def test_enable():
    assert _build_commands("enabled") == ["authentication mac-move deny"]


def test_disable():
    assert _build_commands("disabled") == ["no authentication mac-move deny"]
