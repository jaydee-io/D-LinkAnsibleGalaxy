"""Unit tests for surveillance_vlan_onvif_ipc_description module."""

from surveillance_vlan_onvif_ipc_description import _build_commands


def test_set():
    assert _build_commands("172.18.60.1", None, "ipc1", "present") == [
        "surveillance vlan onvif-ipc 172.18.60.1 description ipc1"]


def test_set_with_mac():
    assert _build_commands("172.18.60.1", "00-01-02-03-04-05", "ipc1", "present") == [
        "surveillance vlan onvif-ipc 172.18.60.1 mac-address 00-01-02-03-04-05 description ipc1"]


def test_remove():
    assert _build_commands("172.18.60.1", None, None, "absent") == [
        "no surveillance vlan onvif-ipc 172.18.60.1 description"]
