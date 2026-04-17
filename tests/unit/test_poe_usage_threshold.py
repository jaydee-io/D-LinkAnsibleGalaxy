"""Unit tests for poe_usage_threshold module command builder."""

from poe_usage_threshold import _build_commands


def test_set():
    assert _build_commands(50, "present") == ["poe usage-threshold 50"]


def test_revert():
    assert _build_commands(None, "absent") == ["no poe usage-threshold"]
