#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jerome Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: show_lldp_neighbor_interface
short_description: Display LLDP neighbor information on a D-Link DGS-1250 switch
description:
  - Executes the C(show lldp neighbors interface) CLI command on a D-Link DGS-1250 switch.
  - Displays LLDP neighbor information learned from the specified interface.
  - Corresponds to CLI command described in chapter 41-24 of the DGS-1250 CLI Reference Guide.
version_added: "0.14.0"
author:
  - Jerome Dumesnil
options:
  interface_id:
    description:
      - The interface ID to display (e.g. C(eth1/0/9)).
    type: str
    required: true
  mode:
    description:
      - C(brief) to display brief information.
      - C(detail) to display detailed information.
      - If not specified, normal mode is used.
    type: str
    choices: [brief, detail]
notes:
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display LLDP neighbor information for interface
  jaydee_io.dlink_dgs1250.show_lldp_neighbor_interface:
    interface_id: eth1/0/9
    mode: detail
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


def _build_command(interface_id, mode):
    cmd = "show lldp neighbors interface %s" % interface_id
    if mode:
        cmd += " %s" % mode
    return cmd


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface_id=dict(type="str", required=True),
            mode=dict(type="str", choices=["brief", "detail"]),
        ),
        supports_check_mode=True,
    )
    command = _build_command(
        module.params["interface_id"], module.params["mode"])
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
