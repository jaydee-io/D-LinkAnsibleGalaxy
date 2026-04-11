"""Unit tests for dhcp_relay_service_dhcp module command builder."""

from dhcp_relay_service_dhcp import _build_commands


def test_enable():
    cmds = _build_commands("enabled")
    assert cmds == ["service dhcp"]


def test_disable():
    cmds = _build_commands("disabled")
    assert cmds == ["no service dhcp"]
