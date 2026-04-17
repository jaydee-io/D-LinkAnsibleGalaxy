"""Unit tests for show_mls_qos_queueing module command builder."""

from show_mls_qos_queueing import _build_command


def test_no_interface():
    assert _build_command(None) == "show mls qos queueing"


def test_with_interface():
    assert _build_command("eth1/0/3") == "show mls qos queueing interface eth1/0/3"
