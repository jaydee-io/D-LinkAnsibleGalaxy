"""Unit tests for mgmt_ip_http_service_port module command builder."""

from mgmt_ip_http_service_port import _build_commands


def test_set_port():
    assert _build_commands(8080, "present") == ["ip http service-port 8080"]


def test_revert():
    assert _build_commands(None, "absent") == ["no ip http service-port"]
