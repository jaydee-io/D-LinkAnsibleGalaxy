"""Unit tests for version module parsers."""

from version import _parse_version

SAMPLE_OUTPUT = """
System MAC Address: F0-7D-68-12-50-01
Module Name DGS-1250-28XMP
H/W A1
Runtime 2.04.P003
"""


def test_parse_version():
    result = _parse_version(SAMPLE_OUTPUT)
    assert result["system_mac_address"] == "F0-7D-68-12-50-01"
    assert result["module_name"] == "DGS-1250-28XMP"
    assert result["hardware_version"] == "A1"
    assert result["runtime"] == "2.04.P003"


def test_parse_version_empty():
    result = _parse_version("")
    assert result["system_mac_address"] == ""
    assert result["module_name"] == ""
    assert result["hardware_version"] == ""
    assert result["runtime"] == ""


def test_parse_version_different_model():
    output = """
System MAC Address: AA-BB-CC-DD-EE-FF
Module Name DGS-1250-52XMP
H/W A2
Runtime 2.10.B001
"""
    result = _parse_version(output)
    assert result["system_mac_address"] == "AA-BB-CC-DD-EE-FF"
    assert result["module_name"] == "DGS-1250-52XMP"
    assert result["hardware_version"] == "A2"
    assert result["runtime"] == "2.10.B001"
