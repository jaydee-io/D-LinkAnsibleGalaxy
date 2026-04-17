"""Unit tests for power_saving module command builder."""

from power_saving import _build_commands


def test_enable_link_detection():
    assert _build_commands("link-detection", "enabled") == ["power-saving link-detection"]


def test_enable_hibernation():
    assert _build_commands("hibernation", "enabled") == ["power-saving hibernation"]


def test_disable_port_shutdown():
    assert _build_commands("port-shutdown", "disabled") == ["no power-saving port-shutdown"]


def test_disable_dim_led():
    assert _build_commands("dim-led", "disabled") == ["no power-saving dim-led"]
