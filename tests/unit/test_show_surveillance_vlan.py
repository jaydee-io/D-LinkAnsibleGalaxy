"""Unit tests for show_surveillance_vlan module."""

from show_surveillance_vlan import _build_command


def test_global():
    assert _build_command(False, None) == "show surveillance vlan"


def test_device():
    assert _build_command(True, None) == "show surveillance vlan device"


def test_interface():
    assert _build_command(False, "eth1/0/1") == "show surveillance vlan interface eth1/0/1"


def test_device_interface():
    assert _build_command(True, "eth1/0/1") == "show surveillance vlan device interface eth1/0/1"
