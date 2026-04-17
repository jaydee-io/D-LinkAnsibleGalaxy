"""Unit tests for storm_control_polling module."""

from storm_control_polling import _build_commands


def test_set_interval():
    assert _build_commands(15, None, "present") == [
        "storm-control polling interval 15"]


def test_set_retries():
    assert _build_commands(None, "infinite", "present") == [
        "storm-control polling retries infinite"]


def test_set_both():
    assert _build_commands(15, "3", "present") == [
        "storm-control polling interval 15",
        "storm-control polling retries 3"]


def test_reset_interval():
    assert _build_commands(5, None, "absent") == [
        "no storm-control polling interval"]


def test_reset_retries():
    assert _build_commands(None, "3", "absent") == [
        "no storm-control polling retries"]
