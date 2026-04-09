"""Unit tests for mgmt_ip_http_server module command builder."""

from mgmt_ip_http_server import _build_commands


def test_enable():
    assert _build_commands("enabled") == ["ip http server"]


def test_disable():
    assert _build_commands("disabled") == ["no ip http server"]
