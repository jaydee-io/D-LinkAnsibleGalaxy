"""Unit tests for service_policy module command builder."""

from service_policy import _build_commands


def test_attach():
    assert _build_commands("eth1/0/1", "cust1-class", "present") == [
        "interface eth1/0/1",
        "service-policy input cust1-class",
        "exit",
    ]


def test_remove():
    assert _build_commands("eth1/0/1", None, "absent") == [
        "interface eth1/0/1",
        "no service-policy input",
        "exit",
    ]
