"""Unit tests for lldp_forward module."""

from lldp_forward import _build_commands


def test_enable():
    assert _build_commands("enabled") == ["lldp forward"]


def test_disable():
    assert _build_commands("disabled") == ["no lldp forward"]
