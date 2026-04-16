"""Unit tests for auth_clear_sessions module command builder."""

from auth_clear_sessions import _build_commands


def test_dot1x():
    assert _build_commands("dot1x", None, None) == ["clear authentication sessions dot1x"]


def test_all():
    assert _build_commands("all", None, None) == ["clear authentication sessions all"]


def test_interface():
    assert _build_commands("interface", "eth1/0/1", None) == [
        "clear authentication sessions interface eth1/0/1"
    ]


def test_mac_address():
    assert _build_commands("mac_address", None, "00-E0-4C-68-2D-6F") == [
        "clear authentication sessions mac-address 00-E0-4C-68-2D-6F"
    ]
