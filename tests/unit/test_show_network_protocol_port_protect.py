"""Unit tests for show_network_protocol_port_protect module command builder."""

from show_network_protocol_port_protect import _build_command


def test_build():
    assert _build_command() == "show network-protocol-port protect"
