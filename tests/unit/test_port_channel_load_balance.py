"""Unit tests for port_channel_load_balance module."""

from port_channel_load_balance import _build_commands


def test_src_ip():
    assert _build_commands("src-ip", "present") == [
        "port-channel load-balance src-ip"
    ]


def test_src_dst_mac():
    assert _build_commands("src-dst-mac", "present") == [
        "port-channel load-balance src-dst-mac"
    ]


def test_absent():
    assert _build_commands(None, "absent") == [
        "no port-channel load-balance"
    ]
