"""Unit tests for show_running_config module."""

from show_running_config import _build_command


def test_basic():
    assert _build_command(None, None, None) == "show running-config"


def test_effective():
    assert _build_command("effective", None, None) == "show running-config effective"


def test_all():
    assert _build_command("all", None, None) == "show running-config all"


def test_interface():
    assert _build_command(None, "eth1/0/1", None) == "show running-config interface eth1/0/1"


def test_vlan():
    assert _build_command(None, None, 100) == "show running-config vlan 100"
