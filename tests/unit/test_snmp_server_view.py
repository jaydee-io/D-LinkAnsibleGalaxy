"""Unit tests for snmp_server_view module command builder."""

from snmp_server_view import _build_commands


def test_create_included():
    assert _build_commands("interfacesMibView", "1.3.6.1.2.1.2", "included", "present") == [
        "snmp-server view interfacesMibView 1.3.6.1.2.1.2 included",
    ]


def test_create_excluded():
    assert _build_commands("myView", "1.3.6.1.6.3", "excluded", "present") == [
        "snmp-server view myView 1.3.6.1.6.3 excluded",
    ]


def test_remove():
    assert _build_commands("interfacesMibView", None, None, "absent") == [
        "no snmp-server view interfacesMibView",
    ]
