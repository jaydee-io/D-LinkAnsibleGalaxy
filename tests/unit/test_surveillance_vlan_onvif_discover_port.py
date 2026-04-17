"""Unit tests for surveillance_vlan_onvif_discover_port module."""

from surveillance_vlan_onvif_discover_port import _build_commands


def test_set():
    assert _build_commands(2000, "present") == ["surveillance vlan onvif-discover-port 2000"]


def test_reset():
    assert _build_commands(None, "absent") == ["no surveillance vlan onvif-discover-port"]
