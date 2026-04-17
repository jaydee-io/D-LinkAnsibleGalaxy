"""Unit tests for snmp_server_community module command builder."""

from snmp_server_community import _build_commands


def test_create_full():
    assert _build_commands("comaccess", "interfacesMibView", "rw", None, "present") == [
        "snmp-server community comaccess view interfacesMibView rw",
    ]


def test_create_simple():
    assert _build_commands("public", None, "ro", None, "present") == [
        "snmp-server community public ro",
    ]


def test_create_with_acl():
    assert _build_commands("public", None, "ro", "myacl", "present") == [
        "snmp-server community public ro access myacl",
    ]


def test_remove():
    assert _build_commands("comaccess", None, None, None, "absent") == [
        "no snmp-server community comaccess",
    ]
