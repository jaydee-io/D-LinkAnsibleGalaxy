"""Unit tests for asymmetric_vlan module command builder."""

from asymmetric_vlan import _build_commands


def test_enable():
    assert _build_commands("enabled") == ["asymmetric-vlan"]


def test_disable():
    assert _build_commands("disabled") == ["no asymmetric-vlan"]
