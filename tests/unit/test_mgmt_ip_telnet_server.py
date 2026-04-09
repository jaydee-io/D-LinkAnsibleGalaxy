"""Unit tests for mgmt_ip_telnet_server module command builder."""

from mgmt_ip_telnet_server import _build_commands


def test_enable():
    assert _build_commands("enabled") == ["ip telnet server"]


def test_disable():
    assert _build_commands("disabled") == ["no ip telnet server"]
