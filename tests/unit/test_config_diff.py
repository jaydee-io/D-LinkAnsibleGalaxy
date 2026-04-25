"""Unit tests for config_diff module."""

from config_diff import _build_commands, _compute_diff


def test_build_commands():
    cmds = _build_commands()
    assert cmds == ["show running-config", "show startup-config"]


def test_compute_diff_identical():
    config = "hostname switch1\nvlan 1\n"
    assert _compute_diff(config, config) == ""


def test_compute_diff_different():
    running = "hostname switch1\nvlan 1\nvlan 100\n"
    startup = "hostname switch1\nvlan 1\n"
    diff = _compute_diff(running, startup)
    assert "--- startup-config" in diff
    assert "+++ running-config" in diff
    assert "+vlan 100" in diff


def test_compute_diff_removed_line():
    running = "hostname switch1\n"
    startup = "hostname switch1\nvlan 1\n"
    diff = _compute_diff(running, startup)
    assert "-vlan 1" in diff


def test_compute_diff_empty_configs():
    assert _compute_diff("", "") == ""


def test_compute_diff_running_empty():
    diff = _compute_diff("", "hostname switch1\n")
    assert "-hostname switch1" in diff


def test_compute_diff_startup_empty():
    diff = _compute_diff("hostname switch1\n", "")
    assert "+hostname switch1" in diff
