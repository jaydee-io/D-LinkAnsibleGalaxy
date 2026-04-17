"""Unit tests for ip_ssh_service_port module command builder."""

from ip_ssh_service_port import _build_commands


def test_set_port():
    assert _build_commands(3000, "present") == [
        "ip ssh service-port 3000",
    ]


def test_revert():
    assert _build_commands(None, "absent") == [
        "no ip ssh service-port",
    ]
