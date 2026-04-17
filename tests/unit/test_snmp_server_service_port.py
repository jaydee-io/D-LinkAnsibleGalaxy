"""Unit tests for snmp_server_service_port module command builder."""

from snmp_server_service_port import _build_commands


def test_set():
    assert _build_commands(50000, "present") == [
        "snmp-server service-port 50000",
    ]


def test_revert():
    assert _build_commands(None, "absent") == [
        "no snmp-server service-port",
    ]
