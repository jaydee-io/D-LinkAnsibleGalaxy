"""Unit tests for ipv6_snooping_station_move_deny module."""

from ipv6_snooping_station_move_deny import _build_commands


def test_enabled():
    assert _build_commands("enabled") == [
        "ipv6 snooping station-move deny"
    ]


def test_disabled():
    assert _build_commands("disabled") == [
        "no ipv6 snooping station-move deny"
    ]
