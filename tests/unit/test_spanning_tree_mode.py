"""Unit tests for spanning_tree_mode module."""

from spanning_tree_mode import _build_commands


def test_set_rstp():
    assert _build_commands("rstp", "present") == ["spanning-tree mode rstp"]


def test_set_mstp():
    assert _build_commands("mstp", "present") == ["spanning-tree mode mstp"]


def test_set_stp():
    assert _build_commands("stp", "present") == ["spanning-tree mode stp"]


def test_reset():
    assert _build_commands(None, "absent") == ["no spanning-tree mode"]
