"""Unit tests for memory_utilization module parsers."""

from memory_utilization import _parse_memory_utilization

SAMPLE_OUTPUT = """
 Memory     Total       Used        Free
--------  ----------  ----------  ----------
 DRAM      243268 K    125316 K    117952 K
 FLASH      45220 K     24968 K     20252 K
"""


def test_parse_memory_utilization():
    memory = _parse_memory_utilization(SAMPLE_OUTPUT)
    assert len(memory) == 2
    assert memory[0] == {
        "type": "DRAM",
        "total_kb": 243268,
        "used_kb": 125316,
        "free_kb": 117952,
    }
    assert memory[1] == {
        "type": "FLASH",
        "total_kb": 45220,
        "used_kb": 24968,
        "free_kb": 20252,
    }


def test_parse_memory_utilization_empty():
    memory = _parse_memory_utilization("")
    assert memory == []


def test_parse_memory_utilization_dram_only():
    output = """
 Memory     Total       Used        Free
--------  ----------  ----------  ----------
 DRAM      512000 K    256000 K    256000 K
"""
    memory = _parse_memory_utilization(output)
    assert len(memory) == 1
    assert memory[0]["type"] == "DRAM"
    assert memory[0]["total_kb"] == 512000
