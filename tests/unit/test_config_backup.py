"""Unit tests for config_backup module command builder."""

from config_backup import _build_command


def test_build_command():
    cmd = _build_command()
    assert cmd == "show running-config"
