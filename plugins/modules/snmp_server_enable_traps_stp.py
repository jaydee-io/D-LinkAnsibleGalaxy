#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: snmp_server_enable_traps_stp
short_description: Enable or disable SNMP STP traps on a D-Link DGS-1250 switch
description:
  - Configures the C(snmp-server enable traps stp) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables sending of SNMP notifications for STP events.
  - Corresponds to CLI command described in chapter 61-4 of the DGS-1250 CLI Reference Guide.
version_added: "0.18.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  trap_types:
    description:
      - List of STP trap types to configure. If omitted, all types are configured.
    type: list
    elements: str
    choices: [new-root, topology-chg]
  state:
    description:
      - C(present) to enable, C(absent) to disable.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable all STP traps
  jaydee_io.dlink_dgs1250.snmp_server_enable_traps_stp:

- name: Enable only new-root traps
  jaydee_io.dlink_dgs1250.snmp_server_enable_traps_stp:
    trap_types:
      - new-root

- name: Disable all STP traps
  jaydee_io.dlink_dgs1250.snmp_server_enable_traps_stp:
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
        run_commands, is_config_present, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, is_config_present, MODE_GLOBAL_CONFIG


def _build_commands(trap_types, state):
    cmd = "snmp-server enable traps stp"
    if trap_types:
        cmd += " " + " ".join(trap_types)
    if state == "absent":
        return ["no " + cmd]
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            trap_types=dict(type="list", elements="str", choices=[
                            "new-root", "topology-chg"]),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["trap_types"], module.params["state"])
    if is_config_present(module, commands):
        module.exit_json(changed=False, commands=[], raw_output="")
        return
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
