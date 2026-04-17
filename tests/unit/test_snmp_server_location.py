"""Unit tests for snmp_server_location module command builder."""

from snmp_server_location import _build_commands


def test_set():
    assert _build_commands("HQ 15F", "present") == [
        "snmp-server location HQ 15F",
    ]


def test_remove():
    assert _build_commands(None, "absent") == [
        "no snmp-server location",
    ]
