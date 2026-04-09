"""Unit tests for mgmt_show_terminal module parser."""

from mgmt_show_terminal import _parse_terminal

SAMPLE_OUTPUT = """
Terminal Settings:
 Length: 24 lines
 width: 80 columns
 Default Length: 24 lines
 Default Width: 80 columns
 Baud Rate: 115200 bps
"""


def test_parse_terminal():
    result = _parse_terminal(SAMPLE_OUTPUT)
    assert result["length"] == 24
    assert result["width"] == 80
    assert result["default_length"] == 24
    assert result["default_width"] == 80
    assert result["baud_rate"] == 115200


def test_parse_empty():
    result = _parse_terminal("")
    assert all(v == 0 for v in result.values())
