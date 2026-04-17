"""Unit tests for configure_replace module."""

from configure_replace import _build_commands


def test_tftp():
    assert _build_commands("tftp", "//10.0.0.66/config.cfg", None, False) == [
        "configure replace tftp: //10.0.0.66/config.cfg"]


def test_flash_force():
    assert _build_commands("flash", None, "Config1", True) == [
        "configure replace flash: Config1 force"]
