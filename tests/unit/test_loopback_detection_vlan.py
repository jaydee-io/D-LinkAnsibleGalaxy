"""Unit tests for loopback_detection_vlan module."""

from loopback_detection_vlan import _build_commands


def test_present():
    assert _build_commands("100-200", "present") == ["loopback-detection vlan 100-200"]


def test_absent():
    assert _build_commands("100-200", "absent") == ["no loopback-detection vlan 100-200"]
