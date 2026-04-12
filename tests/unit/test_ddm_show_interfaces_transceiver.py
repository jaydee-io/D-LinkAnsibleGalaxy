"""Unit tests for ddm_show_interfaces_transceiver module command builder."""

from ddm_show_interfaces_transceiver import _build_command


def test_build_command():
    cmd = _build_command()
    assert cmd == "show interfaces transceiver"
