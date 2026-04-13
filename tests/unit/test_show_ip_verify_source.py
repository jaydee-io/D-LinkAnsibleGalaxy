"""Unit tests for show_ip_verify_source module."""

from show_ip_verify_source import _build_command


def test_no_params():
    assert _build_command(None) == "show ip verify source"


def test_interface():
    assert _build_command("eth1/0/3") == "show ip verify source interface eth1/0/3"
