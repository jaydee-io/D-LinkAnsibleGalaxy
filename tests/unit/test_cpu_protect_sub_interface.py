"""Unit tests for cpu_protect_sub_interface module command builder."""

from cpu_protect_sub_interface import _build_commands


def test_set_rate():
    assert _build_commands("manage", 1000, "present") == [
        "cpu-protect sub-interface manage pps 1000",
    ]


def test_revert():
    assert _build_commands("protocol", None, "absent") == [
        "no cpu-protect sub-interface protocol",
    ]
