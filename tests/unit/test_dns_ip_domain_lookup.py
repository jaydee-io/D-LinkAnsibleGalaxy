"""Unit tests for dns_ip_domain_lookup module command builder."""

from dns_ip_domain_lookup import _build_commands


def test_enable():
    cmds = _build_commands("enabled")
    assert cmds == ["ip domain lookup"]


def test_disable():
    cmds = _build_commands("disabled")
    assert cmds == ["no ip domain lookup"]
