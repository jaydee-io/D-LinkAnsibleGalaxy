"""Unit tests for lldp_fast_count module."""

from lldp_fast_count import _build_commands


def test_set():
    assert _build_commands(10, "present") == ["lldp fast-count 10"]


def test_reset():
    assert _build_commands(None, "absent") == ["no lldp fast-count"]
