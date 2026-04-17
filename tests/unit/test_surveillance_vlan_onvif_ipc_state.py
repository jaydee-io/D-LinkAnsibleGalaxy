"""Unit tests for surveillance_vlan_onvif_ipc_state module."""

from surveillance_vlan_onvif_ipc_state import _build_commands


def test_enable():
    assert _build_commands("172.18.60.1", None, "enabled") == [
        "surveillance vlan onvif-ipc 172.18.60.1 state enable"]


def test_disable_with_mac():
    assert _build_commands("172.18.60.1", "00-01-02-03-04-05", "disabled") == [
        "surveillance vlan onvif-ipc 172.18.60.1 mac-address 00-01-02-03-04-05 state disable"]
