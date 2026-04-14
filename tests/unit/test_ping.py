"""Unit tests for ping module."""

from ping import _build_commands


def test_basic():
    assert _build_commands("211.21.180.1", None, None, None, None) == [
        "ping 211.21.180.1"
    ]


def test_ip_version():
    assert _build_commands("211.21.180.1", "ip", None, None, None) == [
        "ping ip 211.21.180.1"
    ]


def test_ipv6():
    assert _build_commands("2001::1", "ipv6", None, None, None) == [
        "ping ipv6 2001::1"
    ]


def test_count():
    assert _build_commands("211.21.180.1", None, 4, None, None) == [
        "ping 211.21.180.1 count 4"
    ]


def test_timeout():
    assert _build_commands("211.21.180.1", None, None, 5, None) == [
        "ping 211.21.180.1 timeout 5"
    ]


def test_source():
    assert _build_commands("211.21.180.1", None, None, None, "10.1.1.1") == [
        "ping 211.21.180.1 source 10.1.1.1"
    ]


def test_all_params():
    assert _build_commands("211.21.180.1", "ip", 4, 5, "10.1.1.1") == [
        "ping ip 211.21.180.1 count 4 timeout 5 source 10.1.1.1"
    ]
