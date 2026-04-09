"""Unit tests for mgmt_ip_telnet_service_port module command builder."""

from mgmt_ip_telnet_service_port import _build_commands


def test_set_port():
    assert _build_commands(3000, "present") == ["ip telnet service-port 3000"]


def test_revert():
    assert _build_commands(None, "absent") == ["no ip telnet service-port"]
