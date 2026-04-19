#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: clear_counters
short_description: Clear interface counters on a D-Link DGS-1250 switch
description:
  - Executes the C(clear counters) CLI command to clear counters for port interfaces.
  - Corresponds to CLI command described in chapter 30-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.11.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  target:
    description:
      - C(all) clears counters for all interfaces.
      - C(interface) clears counters for a specific interface (requires C(interface_id)).
    type: str
    required: true
    choices: [all, interface]
  interface_id:
    description:
      - The interface(s) to clear counters for. Required when C(target=interface).
    type: str
notes:
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Clear counters on all interfaces
  jaydee_io.dlink_dgs1250.clear_counters:
    target: all

- name: Clear counters on port 1
  jaydee_io.dlink_dgs1250.clear_counters:
    target: interface
    interface_id: eth1/0/1
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
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import (
        run_commands, MODE_PRIVILEGED,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_PRIVILEGED


def _build_commands(target, interface_id):
    if target == "all":
        return ["clear counters all"]
    return ["clear counters interface %s" % interface_id]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            target=dict(type="str", required=True,
                        choices=["all", "interface"]),
            interface_id=dict(type="str"),
        ),
        required_if=[("target", "interface", ["interface_id"])],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["target"], module.params["interface_id"])
    if module.check_mode:
        module.exit_json(changed=True, commands=commands, raw_output="")
        return
    try:
        raw_output = run_commands(module, commands, mode=MODE_PRIVILEGED)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    module.exit_json(changed=True, raw_output=raw_output, commands=commands)


if __name__ == "__main__":
    main()
