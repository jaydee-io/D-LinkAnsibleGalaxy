"""Unit tests for show_ipv6_route module command builder."""

from show_ipv6_route import _build_command


def test_default():
    assert _build_command(None, False) == "show ipv6 route"


def test_connected():
    assert _build_command("connected", False) == "show ipv6 route connected"


def test_database():
    assert _build_command(None, True) == "show ipv6 route database"


def test_static_database():
    assert _build_command("static", True) == "show ipv6 route static database"
