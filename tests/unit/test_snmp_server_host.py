"""Unit tests for snmp_server_host module command builder."""

from snmp_server_host import _build_commands


def test_create_v1():
    assert _build_commands("163.10.50.126", "1", "comaccess", None, "present") == [
        "snmp-server host 163.10.50.126 version 1 comaccess",
    ]


def test_create_v3_auth():
    assert _build_commands("163.10.50.126", "3-auth", "useraccess", None, "present") == [
        "snmp-server host 163.10.50.126 version 3 auth useraccess",
    ]


def test_create_with_port():
    assert _build_commands("163.10.50.126", "1", "comaccess", 50001, "present") == [
        "snmp-server host 163.10.50.126 version 1 comaccess port 50001",
    ]


def test_remove():
    assert _build_commands("163.10.50.126", None, None, None, "absent") == [
        "no snmp-server host 163.10.50.126",
    ]


def test_remove_with_community():
    assert _build_commands("163.10.50.126", None, "comaccess", None, "absent") == [
        "no snmp-server host 163.10.50.126 comaccess",
    ]
