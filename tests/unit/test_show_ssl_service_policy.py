"""Unit tests for show_ssl_service_policy module command builder."""

from show_ssl_service_policy import _build_command


def test_show_all():
    assert _build_command(None) == "show ssl-service-policy"


def test_show_specific():
    assert _build_command("policyForHttp") == "show ssl-service-policy policyForHttp"
