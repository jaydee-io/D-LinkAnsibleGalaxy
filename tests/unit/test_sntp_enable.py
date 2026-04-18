"""Unit tests for sntp_enable module."""

from sntp_enable import _build_commands


def test_enable():
    assert _build_commands("enabled") == ["sntp enable"]


def test_disable():
    assert _build_commands("disabled") == ["no sntp enable"]
