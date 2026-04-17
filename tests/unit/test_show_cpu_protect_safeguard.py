"""Unit tests for show_cpu_protect_safeguard module command builder."""

from show_cpu_protect_safeguard import _build_command


def test_show():
    assert _build_command() == "show cpu-protect safeguard"
