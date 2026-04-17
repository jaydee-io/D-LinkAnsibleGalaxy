"""Unit tests for poe_clear_statistics module command builder."""

from poe_clear_statistics import _build_commands


def test_all():
    assert _build_commands("all", None) == ["clear poe statistic all"]


def test_interface():
    assert _build_commands("interface", "eth1/0/1") == ["clear poe statistic interface eth1/0/1"]
