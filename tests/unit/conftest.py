"""Shared test fixtures: stub Ansible packages so modules can be imported without Ansible installed."""

import sys
import os
import types

# Stub ansible core packages
ansible_stub = types.ModuleType("ansible")
ansible_module_utils = types.ModuleType("ansible.module_utils")
ansible_basic = types.ModuleType("ansible.module_utils.basic")
ansible_basic.AnsibleModule = object
ansible_connection = types.ModuleType("ansible.module_utils.connection")
ansible_connection.Connection = object
ansible_stub.module_utils = ansible_module_utils
ansible_module_utils.basic = ansible_basic
ansible_module_utils.connection = ansible_connection

for mod_name, mod_obj in [
    ("ansible", ansible_stub),
    ("ansible.module_utils", ansible_module_utils),
    ("ansible.module_utils.basic", ansible_basic),
    ("ansible.module_utils.connection", ansible_connection),
]:
    sys.modules.setdefault(mod_name, mod_obj)

# Stub ansible_collections path
for mod in [
    "ansible_collections",
    "ansible_collections.dlink",
    "ansible_collections.jaydee_io.dlink_dgs1250",
    "ansible_collections.jaydee_io.dlink_dgs1250.plugins",
    "ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils",
    "ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250",
]:
    sys.modules.setdefault(mod, types.ModuleType(mod))

# Add module paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "plugins", "modules"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "plugins", "module_utils"))
