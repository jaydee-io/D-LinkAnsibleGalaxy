"""Unit tests for show_surveillance_vlan_onvif_nvr module."""

from show_surveillance_vlan_onvif_nvr import _build_command


def test_basic():
    assert _build_command("eth1/0/1", False) == "show surveillance vlan onvif-nvr interface eth1/0/1"


def test_ipc_list():
    assert _build_command("eth1/0/1", True) == "show surveillance vlan onvif-nvr interface eth1/0/1 ipc-list"


def test_no_interface():
    assert _build_command(None, False) == "show surveillance vlan onvif-nvr interface"
