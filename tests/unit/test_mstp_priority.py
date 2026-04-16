"""Unit tests for mstp_priority module command builder."""

from mstp_priority import _build_commands


def test_set_priority():
    assert _build_commands(2, 0, "present") == ["spanning-tree mst 2 priority 0"]


def test_reset_priority():
    assert _build_commands(2, None, "absent") == ["no spanning-tree mst 2 priority"]
