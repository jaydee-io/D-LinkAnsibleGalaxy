#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: show_interfaces_counters
short_description: Display interface counters on a D-Link DGS-1250 switch
description:
  - Executes the C(show interfaces counters) CLI command on a D-Link DGS-1250 switch.
  - Displays switch port statistics counters, optionally for specific interfaces.
  - Corresponds to CLI command described in chapter 30-7 of the DGS-1250 CLI Reference Guide.
version_added: "0.11.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface_id:
    description:
      - Optional interface(s) to display counters for (e.g. C(eth1/0/1-8)).
      - If not specified, counters for all interfaces are displayed.
    type: str
  errors:
    description:
      - If C(true), display error counters only.
    type: bool
    default: false
notes:
  - This command runs in User/Privileged EXEC Mode.
  - Only physical port interfaces can be specified.
"""

EXAMPLES = r"""
- name: Display counters for ports 1 to 8
  jaydee_io.dlink_dgs1250.show_interfaces_counters:
    interface_id: eth1/0/1-8
  register: result

- name: Display error counters for ports 1 to 8
  jaydee_io.dlink_dgs1250.show_interfaces_counters:
    interface_id: eth1/0/1-8
    errors: true
  register: result
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
        run_command,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _build_command(interface_id, errors):
    cmd = "show interfaces"
    if interface_id:
        cmd += " %s" % interface_id
    cmd += " counters"
    if errors:
        cmd += " errors"
    return cmd


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface_id=dict(type="str"),
            errors=dict(type="bool", default=False),
        ),
        supports_check_mode=True,
    )
    command = _build_command(
        module.params["interface_id"], module.params["errors"])
    if module.check_mode:
        module.exit_json(changed=False, commands=[command], raw_output="")
        return
    try:
        raw_output = run_command(module, command)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    module.exit_json(changed=False, raw_output=raw_output, commands=[command])


if __name__ == "__main__":
    main()
