"""Unit tests for show_ip_route module command builder."""

from show_ip_route import _build_command


def test_default():
    assert _build_command(None, None, None) == "show ip route"


def test_static():
    assert _build_command(None, None, "static") == "show ip route static"


def test_connected():
    assert _build_command(None, None, "connected") == "show ip route connected"


def test_ip():
    assert _build_command("10.0.0.0", None, None) == "show ip route 10.0.0.0"


def test_ip_mask():
    assert _build_command("10.0.0.0", "255.0.0.0", None) == "show ip route 10.0.0.0 255.0.0.0"
