"""Unit tests for mgmt_ip_http_access_class module command builder."""

from mgmt_ip_http_access_class import _build_commands


def test_apply_http():
    assert _build_commands("http", "http-filter", "present") == ["ip http access-class http-filter"]


def test_apply_https():
    assert _build_commands("https", "http-filter", "present") == ["ip https access-class http-filter"]


def test_remove():
    assert _build_commands("http", "http-filter", "absent") == ["no ip http access-class http-filter"]
