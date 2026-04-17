"""Unit tests for poe_policy_preempt module command builder."""

from poe_policy_preempt import _build_commands


def test_enable():
    assert _build_commands("enabled") == ["poe policy preempt"]


def test_disable():
    assert _build_commands("disabled") == ["no poe policy preempt"]
