#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jerome Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: mld_snooping_minimum_version
short_description: Configure MLD snooping minimum version on a D-Link DGS-1250 switch VLAN
description:
  - Configures the C(ipv6 mld snooping minimum-version 2) CLI command on a D-Link DGS-1250 switch.
  - Restricts the minimum version of MLD hosts allowed on a VLAN.
  - Corresponds to CLI command described in chapter 45-12 of the DGS-1250 CLI Reference Guide.
version_added: "0.14.0"
author:
  - Jerome Dumesnil
options:
  vlan_id:
    description:
      - The VLAN ID to configure.
    type: int
    required: true
  state:
    description:
      - C(enabled) to set minimum version to 2 (restrict MLDv1), C(disabled) to remove the restriction.
    type: str
    choices: [enabled, disabled]
    default: enabled
notes:
  - This command runs in VLAN Configuration Mode.
"""

EXAMPLES = r"""
- name: Restrict to MLDv2 only on VLAN 1
  jaydee_io.dlink_dgs1250.mld_snooping_minimum_version:
    vlan_id: 1

- name: Remove minimum version restriction on VLAN 1
  jaydee_io.dlink_dgs1250.mld_snooping_minimum_version:
    vlan_id: 1
    state: disabled
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
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(vlan_id, state):
    cmd = "ipv6 mld snooping minimum-version 2" if state == "enabled" else "no ipv6 mld snooping minimum-version"
    return ["vlan %d" % vlan_id, cmd, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            vlan_id=dict(type="int", required=True),
            state=dict(type="str", choices=[
                       "enabled", "disabled"], default="enabled"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["vlan_id"], module.params["state"])
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
