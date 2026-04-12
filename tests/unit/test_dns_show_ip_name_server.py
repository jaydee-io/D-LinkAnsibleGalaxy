"""Unit tests for dns_show_ip_name_server module command builder."""

from dns_show_ip_name_server import _build_command


def test_build_command():
    cmd = _build_command()
    assert cmd == "show ip name-server"
