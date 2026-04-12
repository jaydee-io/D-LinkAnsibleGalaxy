"""Unit tests for errdisable_recovery module."""

from errdisable_recovery import _build_commands


def test_present_all():
    assert _build_commands("all", None, "present") == ["errdisable recovery cause all"]


def test_present_with_interval():
    assert _build_commands("psecure-violation", 200, "present") == [
        "errdisable recovery cause psecure-violation interval 200"
    ]


def test_present_storm_control():
    assert _build_commands("storm-control", None, "present") == ["errdisable recovery cause storm-control"]


def test_absent():
    assert _build_commands("loopback-detect", None, "absent") == ["no errdisable recovery cause loopback-detect"]


def test_absent_with_interval_ignored():
    assert _build_commands("arp-rate", 100, "absent") == ["no errdisable recovery cause arp-rate"]
