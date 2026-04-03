"""Unit tests for cpu_utilization module parsers."""

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
