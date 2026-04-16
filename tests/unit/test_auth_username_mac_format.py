"""Unit tests for auth_username_mac_format module command builder."""

from auth_username_mac_format import _build_commands


def test_set():
    assert _build_commands("uppercase", "hyphen", 5, "present") == [
        "authentication username mac-format case uppercase delimiter hyphen number 5"
    ]


def test_reset():
    assert _build_commands(None, None, None, "absent") == [
        "no authentication username mac-format"
    ]
