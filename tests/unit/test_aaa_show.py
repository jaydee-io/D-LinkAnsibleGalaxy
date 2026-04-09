"""Unit tests for aaa_show module parser."""

from aaa_show import _parse_aaa


def test_enabled():
    output = "AAA is enabled."
    result = _parse_aaa(output)
    assert result["enabled"] is True


def test_disabled():
    output = "AAA is disabled."
    result = _parse_aaa(output)
    assert result["enabled"] is False


def test_empty():
    result = _parse_aaa("")
    assert result["enabled"] is False
