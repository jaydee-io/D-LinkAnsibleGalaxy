"""Unit tests for snmp_server_contact module command builder."""

from snmp_server_contact import _build_commands


def test_set():
    assert _build_commands("MIS Department II", "present") == [
        "snmp-server contact MIS Department II",
    ]


def test_remove():
    assert _build_commands(None, "absent") == [
        "no snmp-server contact",
    ]
