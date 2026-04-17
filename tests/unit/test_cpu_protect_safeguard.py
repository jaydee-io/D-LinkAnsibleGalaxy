"""Unit tests for cpu_protect_safeguard module command builder."""

from cpu_protect_safeguard import _build_commands


def test_enable_default():
    assert _build_commands(None, None, "enabled") == [
        "cpu-protect safeguard",
    ]


def test_enable_thresholds():
    assert _build_commands(60, 40, "enabled") == [
        "cpu-protect safeguard threshold 60 40",
    ]


def test_disable():
    assert _build_commands(None, None, "disabled") == [
        "no cpu-protect safeguard",
    ]


def test_threshold_absent():
    assert _build_commands(None, None, "threshold_absent") == [
        "no cpu-protect safeguard threshold",
    ]
