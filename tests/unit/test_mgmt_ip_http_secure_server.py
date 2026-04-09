"""Unit tests for mgmt_ip_http_secure_server module command builder."""

from mgmt_ip_http_secure_server import _build_commands


def test_enable():
    assert _build_commands("enabled", None) == ["ip http secure-server"]


def test_enable_with_policy():
    assert _build_commands("enabled", "sp1") == ["ip http secure-server ssl-service-policy sp1"]


def test_disable():
    assert _build_commands("disabled", None) == ["no ip http secure-server"]
