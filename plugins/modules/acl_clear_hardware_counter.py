#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: acl_clear_hardware_counter
short_description: Clear ACL hardware counters on a D-Link DGS-1250 switch
description:
  - Executes the C(clear acl-hardware-counter access-group) CLI command on a D-Link DGS-1250 switch.
  - Clears hardware packet counters for a specific or all access lists.
  - Corresponds to CLI command described in chapter 4-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.3.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  name:
    description:
      - Name or number of the access list to clear.
      - If omitted, all access-group hardware counters are cleared.
    type: str
"""

EXAMPLES = r"""
- name: Clear hardware counter for access-list 'abc'
  jaydee_io.dlink_dgs1250.acl_clear_hardware_counter:
    name: abc

- name: Clear all ACL hardware counters
  jaydee_io.dlink_dgs1250.acl_clear_hardware_counter:
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
commands:
  description: List of CLI commands sent to the switch.
  returned: always
  type: list
  elements: str
"""

from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import run_command
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _build_command(name):
    cmd = "clear acl-hardware-counter access-group"
    if name:
        cmd += " %s" % name
    return cmd


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type="str"),
        ),
        supports_check_mode=True,
    )

    command = _build_command(module.params["name"])
    commands = [command]

    if module.check_mode:
        module.exit_json(changed=True, commands=commands, raw_output="")
        return

    try:
        raw_output = run_command(module, command)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    module.exit_json(changed=True, raw_output=raw_output, commands=commands)


if __name__ == "__main__":
    main()
