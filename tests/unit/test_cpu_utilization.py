"""Unit tests for cpu_utilization module parsers."""

from cpu_utilization import _parse_cpu_utilization

SAMPLE_OUTPUT = """
CPU Utilization
Five seconds -   12 %
One minute -     12 %
Five minutes -   12 %
"""


def test_parse_cpu_utilization():
    result = _parse_cpu_utilization(SAMPLE_OUTPUT)
    assert result["five_seconds_percent"] == 12
    assert result["one_minute_percent"] == 12
    assert result["five_minutes_percent"] == 12


def test_parse_cpu_utilization_different_values():
    output = """
CPU Utilization
Five seconds -   85 %
One minute -     42 %
Five minutes -   23 %
"""
    result = _parse_cpu_utilization(output)
    assert result["five_seconds_percent"] == 85
    assert result["one_minute_percent"] == 42
    assert result["five_minutes_percent"] == 23


def test_parse_cpu_utilization_empty():
    result = _parse_cpu_utilization("")
    assert result["five_seconds_percent"] == 0
    assert result["one_minute_percent"] == 0
    assert result["five_minutes_percent"] == 0
