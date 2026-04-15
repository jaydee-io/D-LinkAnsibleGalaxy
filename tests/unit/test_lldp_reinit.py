"""Unit tests for lldp_reinit module."""

from lldp_reinit import _build_commands


def test_set():
    assert _build_commands(5, "present") == ["lldp reinit 5"]


def test_reset():
    assert _build_commands(None, "absent") == ["no lldp reinit"]
