"""Unit tests for show_cpu_protect_sub_interface module command builder."""

from show_cpu_protect_sub_interface import _build_command


def test_show_manage():
    assert _build_command("manage") == "show cpu-protect sub-interface manage"


def test_show_protocol():
    assert _build_command("protocol") == "show cpu-protect sub-interface protocol"


def test_show_route():
    assert _build_command("route") == "show cpu-protect sub-interface route"
