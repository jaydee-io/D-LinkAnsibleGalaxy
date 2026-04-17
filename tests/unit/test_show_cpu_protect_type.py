"""Unit tests for show_cpu_protect_type module command builder."""

from show_cpu_protect_type import _build_command


def test_show_arp():
    assert _build_command("arp") == "show cpu-protect type arp"
