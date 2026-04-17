"""Unit tests for show_poe_pd_alive module command builder."""

from show_poe_pd_alive import _build_command


def test_default():
    assert _build_command(None) == "show poe pd alive"


def test_interface():
    assert _build_command("eth1/0/1-2") == "show poe pd alive interface eth1/0/1-2"
