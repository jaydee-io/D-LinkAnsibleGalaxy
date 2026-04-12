"""Unit tests for multicast_filtering_mode module."""

from multicast_filtering_mode import _build_commands


def test_present_filter_unregistered():
    assert _build_commands(100, "filter-unregistered", "present") == [
        "vlan 100",
        "multicast filtering-mode filter-unregistered",
        "exit",
    ]


def test_present_forward_all():
    assert _build_commands(1, "forward-all", "present") == [
        "vlan 1",
        "multicast filtering-mode forward-all",
        "exit",
    ]


def test_absent():
    assert _build_commands(100, None, "absent") == [
        "vlan 100",
        "no multicast filtering-mode",
        "exit",
    ]
