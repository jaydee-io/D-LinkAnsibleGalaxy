"""Unit tests for lldp_tx_delay module."""

from lldp_tx_delay import _build_commands


def test_set():
    assert _build_commands(8, "present") == ["lldp tx-delay 8"]


def test_reset():
    assert _build_commands(None, "absent") == ["no lldp tx-delay"]
