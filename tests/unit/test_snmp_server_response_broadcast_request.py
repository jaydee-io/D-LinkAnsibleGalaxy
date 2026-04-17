"""Unit tests for snmp_server_response_broadcast_request module command builder."""

from snmp_server_response_broadcast_request import _build_commands


def test_enable():
    assert _build_commands("enabled") == [
        "snmp-server response broadcast-request",
    ]


def test_disable():
    assert _build_commands("disabled") == [
        "no snmp-server response broadcast-request",
    ]
