"""Unit tests for lacp_system_priority module."""

from lacp_system_priority import _build_commands


def test_present():
    assert _build_commands(30000, "present") == [
        "lacp system-priority 30000"
    ]


def test_absent():
    assert _build_commands(None, "absent") == [
        "no lacp system-priority"
    ]
