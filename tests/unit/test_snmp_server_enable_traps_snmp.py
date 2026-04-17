"""Unit tests for snmp_server_enable_traps_snmp module command builder."""

from snmp_server_enable_traps_snmp import _build_commands


def test_enable_all():
    assert _build_commands(None, "present") == [
        "snmp-server enable traps snmp",
    ]


def test_enable_specific():
    assert _build_commands(["authentication"], "present") == [
        "snmp-server enable traps snmp authentication",
    ]


def test_disable_all():
    assert _build_commands(None, "absent") == [
        "no snmp-server enable traps snmp",
    ]


def test_disable_specific():
    assert _build_commands(["linkup", "linkdown"], "absent") == [
        "no snmp-server enable traps snmp linkup linkdown",
    ]
