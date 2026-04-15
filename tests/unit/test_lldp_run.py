"""Unit tests for lldp_run module."""

from lldp_run import _build_commands


def test_enable():
    assert _build_commands("enabled") == ["lldp run"]


def test_disable():
    assert _build_commands("disabled") == ["no lldp run"]
