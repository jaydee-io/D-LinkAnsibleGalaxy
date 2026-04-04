"""Unit tests for unit module parsers."""

from unit import _parse_model, _parse_unit_info, _parse_memory

SAMPLE_OUTPUT = """
       Model Descr                            Model Name
-------------------------------------------  -----------------------------
 24P 10/100/1000M PoE + 4P 10G SFP+           DGS-1250-28XMP

       Serial-Number                Status        Up Time
---------------------------------  ---------  -----------------
 DGS1250102030                      ok         0DT0H38M59S

 Memory     Total       Used        Free
--------  ----------  ----------  ----------
 DRAM      243268 K    125248 K    118020 K
 FLASH      45220 K     24920 K     20300 K
"""


def test_parse_model():
    model = _parse_model(SAMPLE_OUTPUT)
    assert model["model_description"] == "24P 10/100/1000M PoE + 4P 10G SFP+"
    assert model["model_name"] == "DGS-1250-28XMP"


def test_parse_unit_info():
    unit = _parse_unit_info(SAMPLE_OUTPUT)
    assert unit["serial_number"] == "DGS1250102030"
    assert unit["status"] == "ok"
    assert unit["uptime"] == "0DT0H38M59S"


def test_parse_memory():
    memory = _parse_memory(SAMPLE_OUTPUT)
    assert len(memory) == 2
    assert memory[0] == {
        "type": "DRAM",
        "total_kb": 243268,
        "used_kb": 125248,
        "free_kb": 118020,
    }
    assert memory[1] == {
        "type": "FLASH",
        "total_kb": 45220,
        "used_kb": 24920,
        "free_kb": 20300,
    }
