"""Unit tests for spanning_tree_timers module."""

from spanning_tree_timers import _build_commands


def test_set_hello_time():
    assert _build_commands(1, None, None, "present") == [
        "spanning-tree hello-time 1"]


def test_set_all():
    assert _build_commands(1, 16, 21, "present") == [
        "spanning-tree hello-time 1",
        "spanning-tree forward-time 16",
        "spanning-tree max-age 21"]


def test_reset_hello():
    assert _build_commands(1, None, None, "absent") == [
        "no spanning-tree hello-time"]


def test_reset_all():
    assert _build_commands(1, 1, 1, "absent") == [
        "no spanning-tree hello-time",
        "no spanning-tree forward-time",
        "no spanning-tree max-age"]
