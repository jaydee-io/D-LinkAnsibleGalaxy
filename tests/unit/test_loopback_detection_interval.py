"""Unit tests for loopback_detection_interval module."""

from loopback_detection_interval import _build_commands


def test_set():
    assert _build_commands(20, "present") == ["loopback-detection interval 20"]


def test_reset():
    assert _build_commands(None, "absent") == ["no loopback-detection interval"]
