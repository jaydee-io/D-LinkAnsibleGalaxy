#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: mls_qos_map_dscp_cos
short_description: Configure the DSCP-to-CoS map on a D-Link DGS-1250 switch interface
description:
  - Configures the C(mls qos map dscp-cos) CLI command on a D-Link DGS-1250 switch.
  - Defines a DSCP-to-CoS map on an interface.
  - Corresponds to CLI command described in chapter 54-6 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/6)).
    type: str
    required: true
  dscp_list:
    description:
      - List of DSCP values (0-63) to map, separated by commas or hyphens.
    type: str
    required: true
  cos_value:
    description:
      - CoS value (0-7). Required when C(state=present).
    type: int
  state:
    description:
      - C(present) to set the mapping, C(absent) to revert to the default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Map DSCP 12,16,18 to CoS 1 on port 6
  jaydee_io.dlink_dgs1250.mls_qos_map_dscp_cos:
    interface: eth1/0/6
    dscp_list: "12,16,18"
    cos_value: 1

- name: Revert DSCP mapping on port 6
  jaydee_io.dlink_dgs1250.mls_qos_map_dscp_cos:
    interface: eth1/0/6
    dscp_list: "12,16,18"
    state: absent
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
        run_commands, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(interface, dscp_list, cos_value, state):
    commands = ["interface %s" % interface]
    if state == "absent":
        commands.append("no mls qos map dscp-cos %s" % dscp_list)
    else:
        commands.append("mls qos map dscp-cos %s to %d" % (dscp_list, cos_value))
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            dscp_list=dict(type="str", required=True),
            cos_value=dict(type="int"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["cos_value"])],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interface"],
        module.params["dscp_list"],
        module.params["cos_value"],
        module.params["state"],
    )
    if module.check_mode:
        module.exit_json(changed=True, commands=commands, raw_output="")
        return
    try:
        raw_output = run_commands(module, commands, mode=MODE_GLOBAL_CONFIG)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    module.exit_json(changed=True, raw_output=raw_output, commands=commands)


if __name__ == "__main__":
    main()
