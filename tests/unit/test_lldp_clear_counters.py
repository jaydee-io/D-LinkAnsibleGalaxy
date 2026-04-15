"""Unit tests for lldp_clear_counters module."""

from lldp_clear_counters import _build_commands


def test_clear_all():
    assert _build_commands("all", None) == ["clear lldp counters all"]


def test_clear_interface():
    assert _build_commands("interface", "eth1/0/1") == ["clear lldp counters interface eth1/0/1"]


def test_clear_global():
    assert _build_commands(None, None) == ["clear lldp counters"]
