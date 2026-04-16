"""Unit tests for network_protocol_port_protect module command builder."""

from network_protocol_port_protect import _build_commands


def test_enable_tcp():
    assert _build_commands("tcp", "enabled") == ["network-protocol-port protect tcp"]


def test_disable_udp():
    assert _build_commands("udp", "disabled") == ["no network-protocol-port protect udp"]
