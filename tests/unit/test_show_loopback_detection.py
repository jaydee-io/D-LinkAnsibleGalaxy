"""Unit tests for show_loopback_detection module."""

from show_loopback_detection import _build_command


def test_all():
    assert _build_command(None) == "show loopback-detection"


def test_interface():
    assert _build_command("eth1/0/1") == "show loopback-detection interface eth1/0/1"
