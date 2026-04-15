"""Unit tests for loopback_detection_interface module."""

from loopback_detection_interface import _build_commands


def test_enable():
    assert _build_commands("eth1/0/1", "enabled") == [
        "interface eth1/0/1", "loopback-detection", "exit"]


def test_disable():
    assert _build_commands("eth1/0/1", "disabled") == [
        "interface eth1/0/1", "no loopback-detection", "exit"]
