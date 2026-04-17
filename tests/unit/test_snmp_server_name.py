"""Unit tests for snmp_server_name module command builder."""

from snmp_server_name import _build_commands


def test_set():
    assert _build_commands("SiteA-switch", "present") == [
        "snmp-server name SiteA-switch",
    ]


def test_remove():
    assert _build_commands(None, "absent") == [
        "no snmp-server name",
    ]
