"""Unit tests for speed module."""

from speed import _build_commands


def test_set_auto():
    assert _build_commands("eth1/0/1", "auto", None, None, "present") == [
        "interface eth1/0/1", "speed auto", "exit"]


def test_set_auto_with_list():
    assert _build_commands("eth1/0/1", "auto", None, "10,100", "present") == [
        "interface eth1/0/1", "speed auto 10,100", "exit"]


def test_set_1000_master():
    assert _build_commands("eth1/0/1", "1000", "master", None, "present") == [
        "interface eth1/0/1", "speed 1000 master", "exit"]


def test_set_100():
    assert _build_commands("eth1/0/1", "100", None, None, "present") == [
        "interface eth1/0/1", "speed 100", "exit"]


def test_reset():
    assert _build_commands("eth1/0/1", None, None, None, "absent") == [
        "interface eth1/0/1", "no speed", "exit"]
