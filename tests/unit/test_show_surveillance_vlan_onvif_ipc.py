"""Unit tests for show_surveillance_vlan_onvif_ipc module."""

from show_surveillance_vlan_onvif_ipc import _build_command


def test_brief():
    assert _build_command("eth1/0/1", "brief") == "show surveillance vlan onvif-ipc interface eth1/0/1 brief"


def test_detail():
    assert _build_command(None, "detail") == "show surveillance vlan onvif-ipc interface detail"
