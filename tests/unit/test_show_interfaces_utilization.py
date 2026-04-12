"""Unit tests for show_interfaces_utilization module."""

from show_interfaces_utilization import _build_command


def test_all():
    assert _build_command(None) == "show interfaces utilization"


def test_specific():
    assert _build_command("eth1/0/1-8") == "show interfaces eth1/0/1-8 utilization"
