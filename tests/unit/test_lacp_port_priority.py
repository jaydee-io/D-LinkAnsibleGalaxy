"""Unit tests for lacp_port_priority module."""

from lacp_port_priority import _build_commands


def test_present():
    assert _build_commands("eth1/0/4", 20000, "present") == [
        "interface eth1/0/4",
        "lacp port-priority 20000",
        "exit",
    ]


def test_absent():
    assert _build_commands("eth1/0/4", None, "absent") == [
        "interface eth1/0/4",
        "no lacp port-priority",
        "exit",
    ]
