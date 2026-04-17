"""Unit tests for ipv6_nd_raguard_device_role module command builder."""

from ipv6_nd_raguard_device_role import _build_commands


def test_set_host():
    assert _build_commands("raguard1", "host", "present") == [
        "ipv6 nd raguard policy raguard1",
        "device-role host",
        "exit",
    ]


def test_set_router():
    assert _build_commands("raguard1", "router", "present") == [
        "ipv6 nd raguard policy raguard1",
        "device-role router",
        "exit",
    ]


def test_revert():
    assert _build_commands("raguard1", None, "absent") == [
        "ipv6 nd raguard policy raguard1",
        "no device-role",
        "exit",
    ]
