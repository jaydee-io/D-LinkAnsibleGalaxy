"""Unit tests for mgmt_terminal_speed module command builder."""

from mgmt_terminal_speed import _build_commands


def test_set_speed():
    assert _build_commands(115200, "present") == ["terminal speed 115200"]


def test_remove_speed():
    assert _build_commands(9600, "absent") == ["no terminal speed"]
