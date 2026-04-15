"""Unit tests for loopback_detection_global module."""

from loopback_detection_global import _build_commands


def test_enable():
    assert _build_commands(None, "enabled") == ["loopback-detection"]


def test_enable_port_based():
    assert _build_commands("port-based", "enabled") == [
        "loopback-detection", "loopback-detection mode port-based"]


def test_disable():
    assert _build_commands(None, "disabled") == ["no loopback-detection"]
