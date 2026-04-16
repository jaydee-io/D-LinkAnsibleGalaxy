"""Unit tests for nd_inspection_device_role module command builder."""

from nd_inspection_device_role import _build_commands


def test_set_host():
    assert _build_commands("policy1", "host", "present") == [
        "ipv6 nd inspection policy policy1",
        "device-role host",
        "exit",
    ]


def test_set_router():
    assert _build_commands("policy1", "router", "present") == [
        "ipv6 nd inspection policy policy1",
        "device-role router",
        "exit",
    ]


def test_remove():
    assert _build_commands("policy1", None, "absent") == [
        "ipv6 nd inspection policy policy1",
        "no device-role",
        "exit",
    ]
