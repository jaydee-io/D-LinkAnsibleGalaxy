"""Unit tests for storm_control module."""

from storm_control import _build_commands


def test_broadcast_pps():
    assert _build_commands("eth1/0/1", "broadcast", "pps", 500, None, None, "present") == [
        "interface eth1/0/1", "storm-control broadcast level pps 500", "exit"]


def test_broadcast_percent_with_low():
    assert _build_commands("eth1/0/2", "broadcast", "percent", 70, 60, None, "present") == [
        "interface eth1/0/2", "storm-control broadcast level 70 60", "exit"]


def test_broadcast_kbps():
    assert _build_commands("eth1/0/1", "multicast", "kbps", 1000, None, None, "present") == [
        "interface eth1/0/1", "storm-control multicast level kbps 1000", "exit"]


def test_action_shutdown():
    assert _build_commands("eth1/0/1", None, None, None, None, "shutdown", "present") == [
        "interface eth1/0/1", "storm-control action shutdown", "exit"]


def test_action_drop():
    assert _build_commands("eth1/0/1", None, None, None, None, "drop", "present") == [
        "interface eth1/0/1", "storm-control action drop", "exit"]


def test_remove_broadcast():
    assert _build_commands("eth1/0/1", "broadcast", None, None, None, None, "absent") == [
        "interface eth1/0/1", "no storm-control broadcast", "exit"]


def test_remove_action():
    assert _build_commands("eth1/0/1", None, None, None, None, "shutdown", "absent") == [
        "interface eth1/0/1", "no storm-control action", "exit"]
