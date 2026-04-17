"""Unit tests for show_class_map module command builder."""

from show_class_map import _build_command


def test_no_name():
    assert _build_command(None) == "show class-map"


def test_with_name():
    assert _build_command("c2") == "show class-map c2"
