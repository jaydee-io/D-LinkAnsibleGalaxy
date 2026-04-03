"""Unit tests for snmp_environment_traps module command builder."""

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

from snmp_environment_traps import _build_command


def test_enable_all_traps():
    cmd = _build_command("enabled", False, False, False)
    assert cmd == "snmp-server enable traps environment"


def test_disable_all_traps():
    cmd = _build_command("disabled", False, False, False)
    assert cmd == "no snmp-server enable traps environment"


def test_enable_fan_only():
    cmd = _build_command("enabled", True, False, False)
    assert cmd == "snmp-server enable traps environment fan"


def test_enable_fan_and_temperature():
    cmd = _build_command("enabled", True, False, True)
    assert cmd == "snmp-server enable traps environment fan temperature"


def test_disable_power_only():
    cmd = _build_command("disabled", False, True, False)
    assert cmd == "no snmp-server enable traps environment power"


def test_enable_all_components():
    cmd = _build_command("enabled", True, True, True)
    assert cmd == "snmp-server enable traps environment fan power temperature"
