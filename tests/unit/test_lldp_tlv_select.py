"""Unit tests for lldp_tlv_select module."""

from lldp_tlv_select import _build_commands


def test_enable_all():
    assert _build_commands("eth1/0/1", None, "enabled") == [
        "interface eth1/0/1", "lldp tlv-select", "exit"]


def test_enable_system_name():
    assert _build_commands("eth1/0/1", "system-name", "enabled") == [
        "interface eth1/0/1", "lldp tlv-select system-name", "exit"]


def test_disable_port_description():
    assert _build_commands("eth1/0/1", "port-description", "disabled") == [
        "interface eth1/0/1", "no lldp tlv-select port-description", "exit"]
