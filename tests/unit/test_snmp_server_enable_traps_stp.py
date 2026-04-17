"""Unit tests for snmp_server_enable_traps_stp module."""

from snmp_server_enable_traps_stp import _build_commands


def test_enable_all():
    assert _build_commands(None, "present") == [
        "snmp-server enable traps stp"]


def test_enable_specific():
    assert _build_commands(["new-root"], "present") == [
        "snmp-server enable traps stp new-root"]


def test_disable_all():
    assert _build_commands(None, "absent") == [
        "no snmp-server enable traps stp"]


def test_disable_specific():
    assert _build_commands(["new-root", "topology-chg"], "absent") == [
        "no snmp-server enable traps stp new-root topology-chg"]
