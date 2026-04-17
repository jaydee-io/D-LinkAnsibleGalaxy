"""Unit tests for show_snmp module command builder."""

from show_snmp import _build_command


def test_show_community():
    assert _build_command("community") == "show snmp community"


def test_show_engineID():
    assert _build_command("engineID") == "show snmp engineID"
