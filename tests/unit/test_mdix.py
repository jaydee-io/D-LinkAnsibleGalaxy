"""Unit tests for mdix module."""

from mdix import _build_commands


def test_set_auto():
    assert _build_commands("eth1/0/1", "auto", "present") == [
        "interface eth1/0/1", "mdix auto", "exit"]


def test_set_normal():
    assert _build_commands("eth1/0/1", "normal", "present") == [
        "interface eth1/0/1", "mdix normal", "exit"]


def test_set_cross():
    assert _build_commands("eth1/0/1", "cross", "present") == [
        "interface eth1/0/1", "mdix cross", "exit"]


def test_reset():
    assert _build_commands("eth1/0/1", None, "absent") == [
        "interface eth1/0/1", "no mdix", "exit"]
