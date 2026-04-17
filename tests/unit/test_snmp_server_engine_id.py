"""Unit tests for snmp_server_engine_id module command builder."""

from snmp_server_engine_id import _build_commands


def test_set():
    assert _build_commands("332200000000000000000000", "present") == [
        "snmp-server engineID local 332200000000000000000000",
    ]


def test_revert():
    assert _build_commands(None, "absent") == [
        "no snmp-server engineID local",
    ]
