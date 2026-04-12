"""Unit tests for interface_description module."""

from interface_description import _build_commands


def test_present():
    assert _build_commands("eth1/0/10", "Physical Port 10", "present") == [
        "interface eth1/0/10",
        "description Physical Port 10",
        "exit",
    ]


def test_absent():
    assert _build_commands("eth1/0/10", None, "absent") == [
        "interface eth1/0/10",
        "no description",
        "exit",
    ]
