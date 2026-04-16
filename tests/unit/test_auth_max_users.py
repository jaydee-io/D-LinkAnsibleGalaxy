"""Unit tests for auth_max_users module command builder."""

from auth_max_users import _build_commands


def test_set_global():
    assert _build_commands(None, 256, "present") == ["authentication max users 256"]


def test_set_interface():
    assert _build_commands("eth1/0/1", 10, "present") == [
        "interface eth1/0/1",
        "authentication max users 10",
        "exit",
    ]


def test_reset_global():
    assert _build_commands(None, None, "absent") == ["no authentication max users"]


def test_reset_interface():
    assert _build_commands("eth1/0/1", None, "absent") == [
        "interface eth1/0/1",
        "no authentication max users",
        "exit",
    ]
