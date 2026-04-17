"""Unit tests for duplex module."""

from duplex import _build_commands


def test_set_auto():
    assert _build_commands("eth1/0/1", "auto", "present") == [
        "interface eth1/0/1", "duplex auto", "exit"]


def test_set_full():
    assert _build_commands("eth1/0/1", "full", "present") == [
        "interface eth1/0/1", "duplex full", "exit"]


def test_reset():
    assert _build_commands("eth1/0/1", None, "absent") == [
        "interface eth1/0/1", "no duplex", "exit"]
