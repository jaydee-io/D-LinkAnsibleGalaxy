"""Unit tests for snmp_server_enable_traps_storm_control module."""

from snmp_server_enable_traps_storm_control import _build_commands


def test_enable_all():
    assert _build_commands(None, "present") == [
        "snmp-server enable traps storm-control"]


def test_enable_specific():
    assert _build_commands(["storm-occur"], "present") == [
        "snmp-server enable traps storm-control storm-occur"]


def test_disable_all():
    assert _build_commands(None, "absent") == [
        "no snmp-server enable traps storm-control"]
