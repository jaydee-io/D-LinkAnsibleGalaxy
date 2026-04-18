"""Unit tests for logging_server module."""

from logging_server import _build_commands


def test_add_simple():
    assert _build_commands("20.3.3.3", None, None, None, None, "present") == [
        "logging server 20.3.3.3"]


def test_add_with_severity():
    assert _build_commands("20.3.3.3", "warnings", None, None, None, "present") == [
        "logging server 20.3.3.3 severity warnings"]


def test_add_all_options():
    assert _build_commands("20.3.3.3", "errors", 23, "myfilter", 1514, "present") == [
        "logging server 20.3.3.3 severity errors facility 23 discriminator myfilter port 1514"]


def test_remove():
    assert _build_commands("20.3.3.3", None, None, None, None, "absent") == [
        "no logging server 20.3.3.3"]
