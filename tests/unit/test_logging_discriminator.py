"""Unit tests for logging_discriminator module."""

from logging_discriminator import _build_commands


def test_create_with_facility_and_severity():
    assert _build_commands("buffer-filter", "includes", "STP", "includes", "14,6", "present") == [
        "logging discriminator buffer-filter facility includes STP severity includes 14,6"]


def test_create_simple():
    assert _build_commands("mydisc", None, None, None, None, "present") == [
        "logging discriminator mydisc"]


def test_create_facility_only():
    assert _build_commands("mydisc", "drops", "AAA", None, None, "present") == [
        "logging discriminator mydisc facility drops AAA"]


def test_remove():
    assert _build_commands("buffer-filter", None, None, None, None, "absent") == [
        "no logging discriminator buffer-filter"]
