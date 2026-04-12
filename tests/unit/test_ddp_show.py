"""Unit tests for ddp_show module command builder."""

from ddp_show import _build_command


def test_build_command():
    cmd = _build_command()
    assert cmd == "show ddp"
