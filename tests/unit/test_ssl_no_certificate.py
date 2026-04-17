"""Unit tests for ssl_no_certificate module command builder."""

from ssl_no_certificate import _build_commands


def test_delete_certificate():
    assert _build_commands("gaa", "tongken.ca") == [
        "crypto pki certificate chain gaa",
        "no certificate tongken.ca",
        "exit",
    ]
