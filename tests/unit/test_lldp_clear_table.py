"""Unit tests for lldp_clear_table module."""

from lldp_clear_table import _build_commands


def test_clear_all():
    assert _build_commands("all", None) == ["clear lldp table all"]


def test_clear_interface():
    assert _build_commands("interface", "eth1/0/1") == ["clear lldp table interface eth1/0/1"]
