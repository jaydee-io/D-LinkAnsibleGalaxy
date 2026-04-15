"""Unit tests for show_lldp_local_interface module."""

from show_lldp_local_interface import _build_command


def test_normal():
    assert _build_command("eth1/0/1", None) == "show lldp local interface eth1/0/1"


def test_detail():
    assert _build_command("eth1/0/1", "detail") == "show lldp local interface eth1/0/1 detail"


def test_brief():
    assert _build_command("eth1/0/1", "brief") == "show lldp local interface eth1/0/1 brief"
