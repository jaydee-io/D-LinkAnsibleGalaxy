"""Unit tests for autoconfig_show module command builder."""

from autoconfig_show import _build_command


def test_build_command():
    cmd = _build_command()
    assert cmd == "show autoconfig"
