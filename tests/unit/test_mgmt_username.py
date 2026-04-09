"""Unit tests for mgmt_username module command builder."""

from mgmt_username import _build_commands


def test_create_with_password():
    assert _build_commands("admin", "Secret", None, False, "present") == [
        "username admin password Secret",
    ]


def test_create_with_encrypted_password():
    assert _build_commands("admin", "Secret", 7, False, "present") == [
        "username admin password 7 Secret",
    ]


def test_create_nopassword():
    assert _build_commands("guest", None, None, True, "present") == [
        "username guest nopassword",
    ]


def test_remove_user():
    assert _build_commands("guest", None, None, False, "absent") == [
        "no username guest",
    ]


def test_create_without_password():
    assert _build_commands("viewer", None, None, False, "present") == [
        "username viewer",
    ]
