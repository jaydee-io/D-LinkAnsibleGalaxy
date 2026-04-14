"""Unit tests for ping_access_class module."""

from ping_access_class import _build_commands


def test_present():
    assert _build_commands("ping-filter", "present") == [
        "ping access-class ping-filter"
    ]


def test_absent():
    assert _build_commands("ping-filter", "absent") == [
        "no ping access-class ping-filter"
    ]
