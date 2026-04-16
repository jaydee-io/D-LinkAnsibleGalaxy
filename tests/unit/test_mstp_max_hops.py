"""Unit tests for mstp_max_hops module command builder."""

from mstp_max_hops import _build_commands


def test_set_hops():
    assert _build_commands(19, "present") == ["spanning-tree mst max-hops 19"]


def test_reset_hops():
    assert _build_commands(None, "absent") == ["no spanning-tree mst max-hops"]
