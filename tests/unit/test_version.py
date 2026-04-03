"""Unit tests for version module parsers."""

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
