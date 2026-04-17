"""Unit tests for ssl_service_policy module command builder."""

from ssl_service_policy import _build_commands


def test_set_trustpoint():
    assert _build_commands("ssl-server", None, None, "TP1", None, "present") == [
        "ssl-service-policy ssl-server secure-trustpoint TP1",
    ]


def test_set_version():
    assert _build_commands("pol1", "tls1.2", None, None, None, "present") == [
        "ssl-service-policy pol1 version tls1.2",
    ]


def test_set_timeout():
    assert _build_commands("pol1", None, None, None, 1200, "present") == [
        "ssl-service-policy pol1 session-cache-timeout 1200",
    ]


def test_remove():
    assert _build_commands("ssl-server", None, None, None, None, "absent") == [
        "no ssl-service-policy ssl-server",
    ]


def test_remove_with_options():
    assert _build_commands("ssl-server", None, None, "TP1", None, "absent") == [
        "no ssl-service-policy ssl-server secure-trustpoint TP1",
    ]
