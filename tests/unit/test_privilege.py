"""Unit tests for privilege module parsers."""

from privilege import _parse_privilege

SAMPLE_OUTPUT = """
Current level is privilege level
"""


def test_parse_privilege():
    result = _parse_privilege(SAMPLE_OUTPUT)
    assert result == "privilege level"


def test_parse_privilege_empty():
    result = _parse_privilege("")
    assert result == ""


def test_parse_privilege_user_level():
    output = "Current level is user level"
    result = _parse_privilege(output)
    assert result == "user level"
