"""Unit tests for mgmt_service_password_encryption module command builder."""

from mgmt_service_password_encryption import _build_commands


def test_enable():
    assert _build_commands("enabled", None) == ["service password-encryption"]


def test_enable_md5():
    assert _build_commands("enabled", 15) == ["service password-encryption 15"]


def test_enable_sha1():
    assert _build_commands("enabled", 7) == ["service password-encryption 7"]


def test_disable():
    assert _build_commands("disabled", None) == ["no service password-encryption"]
