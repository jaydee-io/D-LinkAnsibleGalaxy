"""Unit tests for memory_utilization module parsers."""

import sys
import os
import types
import pytest

# Stub the ansible package so the module can be imported without Ansible installed
ansible_stub = types.ModuleType("ansible")
ansible_module_utils = types.ModuleType("ansible.module_utils")
ansible_basic = types.ModuleType("ansible.module_utils.basic")
ansible_basic.AnsibleModule = object
ansible_stub.module_utils = ansible_module_utils
ansible_module_utils.basic = ansible_basic
sys.modules.setdefault("ansible", ansible_stub)
sys.modules.setdefault("ansible.module_utils", ansible_module_utils)
sys.modules.setdefault("ansible.module_utils.basic", ansible_basic)

for mod in [
    "ansible_collections",
    "ansible_collections.dlink",
    "ansible_collections.dlink.dgs1250",
    "ansible_collections.dlink.dgs1250.plugins",
    "ansible_collections.dlink.dgs1250.plugins.module_utils",
    "ansible_collections.dlink.dgs1250.plugins.module_utils.dgs1250",
]:
    sys.modules.setdefault(mod, types.ModuleType(mod))

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "plugins", "modules"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "plugins", "module_utils"))

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
