"""Unit tests for vlan_acceptable_frame module."""

from vlan_acceptable_frame import _build_commands


def test_set_tagged_only():
    assert _build_commands("eth1/0/1", "tagged-only", "present") == [
        "interface eth1/0/1", "acceptable-frame tagged-only", "exit"]


def test_set_admit_all():
    assert _build_commands("eth1/0/1", "admit-all", "present") == [
        "interface eth1/0/1", "acceptable-frame admit-all", "exit"]


def test_absent():
    assert _build_commands("eth1/0/1", None, "absent") == [
        "interface eth1/0/1", "no acceptable-frame", "exit"]
