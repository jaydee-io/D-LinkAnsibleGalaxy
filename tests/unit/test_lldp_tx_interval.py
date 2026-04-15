"""Unit tests for lldp_tx_interval module."""

from lldp_tx_interval import _build_commands


def test_set():
    assert _build_commands(50, "present") == ["lldp tx-interval 50"]


def test_reset():
    assert _build_commands(None, "absent") == ["no lldp tx-interval"]
