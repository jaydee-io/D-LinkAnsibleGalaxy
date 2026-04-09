"""Unit tests for ipv6_nd_other_config_flag module command builder."""

from ipv6_nd_other_config_flag import _build_commands


def test_enabled():
    assert _build_commands("vlan1", "enabled") == [
        "interface vlan1",
        "ipv6 nd other-config-flag",
        "exit",
    ]


def test_disabled():
    assert _build_commands("vlan1", "disabled") == [
        "interface vlan1",
        "no ipv6 nd other-config-flag",
        "exit",
    ]
