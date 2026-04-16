"""Unit tests for auth_username module command builder."""

from auth_username import _build_commands


def test_create():
    assert _build_commands("user1", "pass1", None, "present") == [
        "authentication username user1 password pass1"
    ]


def test_create_with_vlan():
    assert _build_commands("user1", "pass1", 10, "present") == [
        "authentication username user1 password pass1 vlan 10"
    ]


def test_remove():
    assert _build_commands("user1", None, None, "absent") == [
        "no authentication username user1"
    ]
