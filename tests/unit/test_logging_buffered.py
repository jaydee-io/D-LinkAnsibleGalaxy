"""Unit tests for logging_buffered module."""

from logging_buffered import _build_commands


def test_enable_default():
    assert _build_commands(None, None, None, "enabled") == ["logging buffered"]


def test_enable_severity():
    assert _build_commands("errors", None, None, "enabled") == ["logging buffered severity errors"]


def test_enable_discriminator():
    assert _build_commands(None, "myfilter", None, "enabled") == ["logging buffered discriminator myfilter"]


def test_enable_write_delay():
    assert _build_commands(None, None, "300", "enabled") == ["logging buffered write-delay 300"]


def test_enable_all_options():
    assert _build_commands("warnings", "myfilter", "infinite", "enabled") == [
        "logging buffered severity warnings discriminator myfilter write-delay infinite"]


def test_disable():
    assert _build_commands(None, None, None, "disabled") == ["no logging buffered"]


def test_default():
    assert _build_commands(None, None, None, "default") == ["default logging buffered"]
