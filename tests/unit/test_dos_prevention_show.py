"""Unit tests for dos_prevention_show module command builder."""

from dos_prevention_show import _build_command


def test_build_command():
    cmd = _build_command()
    assert cmd == "show dos-prevention"
