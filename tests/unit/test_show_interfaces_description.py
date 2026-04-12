"""Unit tests for show_interfaces_description module."""

from show_interfaces_description import _build_command


def test_all():
    assert _build_command(None) == "show interfaces description"


def test_specific():
    assert _build_command("eth1/0/1") == "show interfaces eth1/0/1 description"
