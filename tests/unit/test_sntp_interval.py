"""Unit tests for sntp_interval module."""

from sntp_interval import _build_commands


def test_set():
    assert _build_commands(100, "present") == ["sntp interval 100"]


def test_absent():
    assert _build_commands(None, "absent") == ["no sntp interval"]
