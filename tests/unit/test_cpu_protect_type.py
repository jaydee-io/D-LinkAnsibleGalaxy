"""Unit tests for cpu_protect_type module command builder."""

from cpu_protect_type import _build_commands


def test_set_rate():
    assert _build_commands("arp", 100, "present") == [
        "cpu-protect type arp pps 100",
    ]


def test_revert():
    assert _build_commands("arp", None, "absent") == [
        "no cpu-protect type arp",
    ]
