"""Unit tests for ipv4_arp module command builder."""

from ipv4_arp import _build_commands


def test_present():
    assert _build_commands("10.0.0.1", "00-11-22-33-44-55", "present") == [
        "arp 10.0.0.1 00-11-22-33-44-55",
    ]


def test_absent():
    assert _build_commands("10.0.0.1", "00-11-22-33-44-55", "absent") == [
        "no arp 10.0.0.1 00-11-22-33-44-55",
    ]
