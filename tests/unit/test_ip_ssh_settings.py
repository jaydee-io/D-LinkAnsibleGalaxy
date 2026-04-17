"""Unit tests for ip_ssh_settings module command builder."""

from ip_ssh_settings import _build_commands


def test_set_timeout():
    assert _build_commands(160, None, "present") == [
        "ip ssh timeout 160",
    ]


def test_set_retries():
    assert _build_commands(None, 2, "present") == [
        "ip ssh authentication-retries 2",
    ]


def test_set_both():
    assert _build_commands(160, 2, "present") == [
        "ip ssh timeout 160",
        "ip ssh authentication-retries 2",
    ]


def test_revert():
    assert _build_commands(None, None, "absent") == [
        "no ip ssh timeout",
        "no ip ssh authentication-retries",
    ]
