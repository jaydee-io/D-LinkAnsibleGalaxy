"""Unit tests for environment_temperature_threshold module command builder."""

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

from environment_temperature_threshold import _build_command


def test_set_both_thresholds():
    cmd = _build_command("present", 100, 20)
    assert cmd == "environment temperature threshold thermal high 100 low 20"


def test_set_high_only():
    cmd = _build_command("present", 80, None)
    assert cmd == "environment temperature threshold thermal high 80"


def test_set_low_only():
    cmd = _build_command("present", None, 10)
    assert cmd == "environment temperature threshold thermal low 10"


def test_reset_both_thresholds():
    cmd = _build_command("absent", None, None)
    assert cmd == "no environment temperature threshold thermal high low"


def test_reset_high_only():
    cmd = _build_command("absent", 100, None)
    assert cmd == "no environment temperature threshold thermal high"


def test_reset_low_only():
    cmd = _build_command("absent", None, 10)
    assert cmd == "no environment temperature threshold thermal low"


def test_negative_thresholds():
    cmd = _build_command("present", 50, -20)
    assert cmd == "environment temperature threshold thermal high 50 low -20"
