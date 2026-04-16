"""Unit tests for show_auth_sessions module command builder."""

from show_auth_sessions import _build_command


def test_default():
    assert _build_command(False, None, None) == "show authentication sessions"


def test_dot1x():
    assert _build_command(True, None, None) == "show authentication sessions dot1x"


def test_interface():
    assert _build_command(False, "eth1/0/1", None) == \
        "show authentication sessions interface eth1/0/1"


def test_mac_address():
    assert _build_command(False, None, "00-E0-4C-68-2D-6F") == \
        "show authentication sessions mac-address 00-E0-4C-68-2D-6F"
