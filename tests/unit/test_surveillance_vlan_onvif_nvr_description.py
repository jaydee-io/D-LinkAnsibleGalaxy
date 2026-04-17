"""Unit tests for surveillance_vlan_onvif_nvr_description module."""

from surveillance_vlan_onvif_nvr_description import _build_commands


def test_set():
    assert _build_commands("172.18.60.2", None, "nvr1", "present") == [
        "surveillance vlan onvif-nvr 172.18.60.2 description nvr1"]


def test_set_with_mac():
    assert _build_commands("172.18.60.2", "00-03-02-03-04-08", "nvr1", "present") == [
        "surveillance vlan onvif-nvr 172.18.60.2 mac-address 00-03-02-03-04-08 description nvr1"]


def test_remove():
    assert _build_commands("172.18.60.2", None, None, "absent") == [
        "no surveillance vlan onvif-nvr 172.18.60.2 description"]
