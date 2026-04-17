"""Unit tests for ip_route module command builder."""

from ip_route import _build_commands


def test_add():
    assert _build_commands("20.0.0.0", "255.0.0.0", "10.1.1.254", None, "present") == [
        "ip route 20.0.0.0 255.0.0.0 10.1.1.254",
    ]


def test_add_primary():
    assert _build_commands("20.0.0.0", "255.0.0.0", "10.1.1.254", "primary", "present") == [
        "ip route 20.0.0.0 255.0.0.0 10.1.1.254 primary",
    ]


def test_add_backup():
    assert _build_commands("20.0.0.0", "255.0.0.0", "10.1.1.254", "backup", "present") == [
        "ip route 20.0.0.0 255.0.0.0 10.1.1.254 backup",
    ]


def test_remove():
    assert _build_commands("20.0.0.0", "255.0.0.0", "10.1.1.254", None, "absent") == [
        "no ip route 20.0.0.0 255.0.0.0 10.1.1.254",
    ]
