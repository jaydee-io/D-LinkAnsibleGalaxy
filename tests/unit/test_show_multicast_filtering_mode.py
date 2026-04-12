"""Unit tests for show_multicast_filtering_mode module."""

from show_multicast_filtering_mode import _build_command


def test_all_vlans():
    assert _build_command(None) == "show multicast filtering-mode"


def test_specific_vlan():
    assert _build_command(100) == "show multicast filtering-mode interface 100"
