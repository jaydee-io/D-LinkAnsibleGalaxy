"""Unit tests for boot_config module."""

from boot_config import _build_commands


def test_config1():
    assert _build_commands("Config1") == ["boot config Config1"]


def test_config2():
    assert _build_commands("Config2") == ["boot config Config2"]
