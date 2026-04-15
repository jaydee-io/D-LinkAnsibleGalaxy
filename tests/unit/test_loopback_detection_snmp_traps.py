"""Unit tests for loopback_detection_snmp_traps module."""

from loopback_detection_snmp_traps import _build_commands


def test_enable():
    assert _build_commands("enabled") == ["snmp-server enable traps loopback-detection"]


def test_disable():
    assert _build_commands("disabled") == ["no snmp-server enable traps loopback-detection"]
