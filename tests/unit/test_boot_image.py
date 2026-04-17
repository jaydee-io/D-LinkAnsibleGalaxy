"""Unit tests for boot_image module."""

from boot_image import _build_commands


def test_image1():
    assert _build_commands("Image1", False) == ["boot image Image1"]


def test_image2_check():
    assert _build_commands("Image2", True) == ["boot image check Image2"]
