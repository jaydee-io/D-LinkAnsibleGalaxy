"""Unit tests for clear_cpu_protect_counters module command builder."""

from clear_cpu_protect_counters import _build_commands


def test_clear_all():
    assert _build_commands("all", None, None) == [
        "clear cpu-protect counters all",
    ]


def test_clear_sub_interface_all():
    assert _build_commands("sub-interface", None, None) == [
        "clear cpu-protect counters sub-interface",
    ]


def test_clear_sub_interface_manage():
    assert _build_commands("sub-interface", "manage", None) == [
        "clear cpu-protect counters sub-interface manage",
    ]


def test_clear_type_all():
    assert _build_commands("type", None, None) == [
        "clear cpu-protect counters type",
    ]


def test_clear_type_arp():
    assert _build_commands("type", None, "arp") == [
        "clear cpu-protect counters type arp",
    ]
