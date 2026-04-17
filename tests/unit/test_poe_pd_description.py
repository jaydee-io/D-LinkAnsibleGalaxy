"""Unit tests for poe_pd_description module command builder."""

from poe_pd_description import _build_commands


def test_set_description():
    assert _build_commands("eth1/0/1", "For VoIP usage", "present") == [
        "interface eth1/0/1",
        "poe pd description For VoIP usage",
        "exit",
    ]


def test_clear_description():
    assert _build_commands("eth1/0/1", None, "absent") == [
        "interface eth1/0/1",
        "no poe pd description",
        "exit",
    ]
