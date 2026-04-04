"""Unit tests for environment_temperature_threshold module command builder."""

from environment_temperature_threshold import _build_command


def test_set_both_thresholds():
    cmd = _build_command("present", 100, 20)
    assert cmd == "environment temperature threshold thermal high 100 low 20"


def test_set_high_only():
    cmd = _build_command("present", 80, None)
    assert cmd == "environment temperature threshold thermal high 80"


def test_set_low_only():
    cmd = _build_command("present", None, 10)
    assert cmd == "environment temperature threshold thermal low 10"


def test_reset_both_thresholds():
    cmd = _build_command("absent", None, None)
    assert cmd == "no environment temperature threshold thermal high low"


def test_reset_high_only():
    cmd = _build_command("absent", 100, None)
    assert cmd == "no environment temperature threshold thermal high"


def test_reset_low_only():
    cmd = _build_command("absent", None, 10)
    assert cmd == "no environment temperature threshold thermal low"


def test_negative_thresholds():
    cmd = _build_command("present", 50, -20)
    assert cmd == "environment temperature threshold thermal high 50 low -20"
