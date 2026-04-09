"""Unit tests for mgmt_password module command builder."""

from mgmt_password import _build_commands


def test_set_password():
    assert _build_commands("telnet", "MyPass", None, "present") == [
        "line telnet",
        "password MyPass",
        "exit",
    ]


def test_set_encrypted_password():
    assert _build_commands("ssh", "EncPass", 15, "present") == [
        "line ssh",
        "password 15 EncPass",
        "exit",
    ]


def test_remove_password():
    assert _build_commands("console", None, None, "absent") == [
        "line console",
        "no password",
        "exit",
    ]
