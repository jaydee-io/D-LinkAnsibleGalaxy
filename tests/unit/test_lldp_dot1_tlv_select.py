"""Unit tests for lldp_dot1_tlv_select module."""

from lldp_dot1_tlv_select import _build_commands


def test_enable_port_vlan():
    assert _build_commands("eth1/0/1", "port-vlan", None, None, "enabled") == [
        "interface eth1/0/1", "lldp dot1-tlv-select port-vlan", "exit"]


def test_disable_port_vlan():
    assert _build_commands("eth1/0/1", "port-vlan", None, None, "disabled") == [
        "interface eth1/0/1", "no lldp dot1-tlv-select port-vlan", "exit"]


def test_enable_vlan_name():
    assert _build_commands("eth1/0/1", "vlan-name", "1-3", None, "enabled") == [
        "interface eth1/0/1", "lldp dot1-tlv-select vlan-name 1-3", "exit"]


def test_enable_protocol_identity_lacp():
    assert _build_commands("eth1/0/1", "protocol-identity", None, "lacp", "enabled") == [
        "interface eth1/0/1", "lldp dot1-tlv-select protocol-identity lacp", "exit"]


def test_enable_protocol_identity_no_name():
    assert _build_commands("eth1/0/1", "protocol-identity", None, None, "enabled") == [
        "interface eth1/0/1", "lldp dot1-tlv-select protocol-identity", "exit"]
