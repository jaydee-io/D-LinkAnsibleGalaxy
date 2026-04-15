"""Unit tests for lldp_management_address module."""

from lldp_management_address import _build_commands


def test_set_ipv4():
    assert _build_commands("eth1/0/1", "10.1.1.1", "present") == [
        "interface eth1/0/1", "lldp management-address 10.1.1.1", "exit"]


def test_remove_ipv4():
    assert _build_commands("eth1/0/1", "10.1.1.1", "absent") == [
        "interface eth1/0/1", "no lldp management-address 10.1.1.1", "exit"]


def test_remove_all():
    assert _build_commands("eth1/0/1", None, "absent") == [
        "interface eth1/0/1", "no lldp management-address", "exit"]
