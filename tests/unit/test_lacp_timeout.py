"""Unit tests for lacp_timeout module."""

from lacp_timeout import _build_commands


def test_short():
    assert _build_commands("eth1/0/1", "short", "present") == [
        "interface eth1/0/1",
        "lacp timeout short",
        "exit",
    ]


def test_long():
    assert _build_commands("eth1/0/1", "long", "present") == [
        "interface eth1/0/1",
        "lacp timeout long",
        "exit",
    ]


def test_absent():
    assert _build_commands("eth1/0/1", None, "absent") == [
        "interface eth1/0/1",
        "no lacp timeout",
        "exit",
    ]
