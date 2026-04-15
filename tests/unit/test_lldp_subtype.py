"""Unit tests for lldp_subtype module."""

from lldp_subtype import _build_commands


def test_mac_address():
    assert _build_commands("eth1/0/1", "mac-address") == [
        "interface eth1/0/1", "lldp subtype port-id mac-address", "exit"]


def test_local():
    assert _build_commands("eth1/0/1", "local") == [
        "interface eth1/0/1", "lldp subtype port-id local", "exit"]
