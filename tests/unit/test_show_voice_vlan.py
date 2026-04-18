"""Unit tests for show_voice_vlan module."""

from show_voice_vlan import _build_command


def test_global():
    assert _build_command("global", None) == "show voice vlan"


def test_interface():
    assert _build_command("interface", "eth1/0/1-5") == "show voice vlan interface eth1/0/1-5"


def test_interface_no_port():
    assert _build_command("interface", None) == "show voice vlan interface"


def test_device():
    assert _build_command("device", None) == "show voice vlan device"


def test_device_interface():
    assert _build_command("device", "eth1/0/1-2") == "show voice vlan device interface eth1/0/1-2"


def test_lldp_med_device():
    assert _build_command("lldp_med_device", None) == "show voice vlan lldp-med device"


def test_lldp_med_device_interface():
    assert _build_command("lldp_med_device", "eth1/0/1-2") == "show voice vlan lldp-med device interface eth1/0/1-2"
