"""Unit tests for mgmt_show_ip_telnet_server module parser."""

from mgmt_show_ip_telnet_server import _parse_server_state


def test_enabled():
    assert _parse_server_state("Server State: Enabled") is True


def test_disabled():
    assert _parse_server_state("Server State: Disabled") is False


def test_empty():
    assert _parse_server_state("") is False
