"""Unit tests for show_policy_map module command builder."""

from show_policy_map import _build_command


def test_no_args():
    assert _build_command(None, None) == "show policy-map"


def test_policy_name():
    assert _build_command("policy1", None) == "show policy-map policy1"


def test_interface():
    assert _build_command(None, "eth1/0/1") == "show policy-map interface eth1/0/1"
