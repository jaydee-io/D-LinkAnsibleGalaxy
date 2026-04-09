"""Unit tests for mgmt_ip_http_timeout module command builder."""

from mgmt_ip_http_timeout import _build_commands


def test_set_timeout():
    assert _build_commands(100, "present") == ["ip http timeout-policy idle 100"]


def test_revert():
    assert _build_commands(None, "absent") == ["no ip http timeout-policy idle"]
