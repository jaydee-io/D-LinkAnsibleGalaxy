"""Unit tests for file_copy module."""

from file_copy import _build_commands


def test_save_running():
    assert _build_commands("running-config", "startup-config") == [
        "copy running-config startup-config"]


def test_tftp_download():
    assert _build_commands("tftp: //10.1.1.254/config.cfg", "running-config") == [
        "copy tftp: //10.1.1.254/config.cfg running-config"]
