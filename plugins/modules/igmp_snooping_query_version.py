#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: igmp_snooping_query_version
short_description: Configure IGMP snooping query version on a D-Link DGS-1250 switch
description:
  - Configures the C(ip igmp snooping query-version) CLI command on a D-Link DGS-1250 switch.
  - Sets the general query packet version sent by the IGMP snooping querier on a VLAN.
  - Corresponds to CLI command described in chapter 31-9 of the DGS-1250 CLI Reference Guide.
version_added: "0.12.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  vlan_id:
    description:
      - The VLAN ID to configure.
    type: int
    required: true
  version:
    description:
      - The IGMP query version (1 to 3). Required when C(state=present).
    type: int
  state:
    description:
      - C(present) to set the version, C(absent) to revert to default (3).
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in VLAN Configuration Mode.
"""

EXAMPLES = r"""
- name: Set IGMP snooping query version to 2 on VLAN 1000
  jaydee_io.dlink_dgs1250.igmp_snooping_query_version:
    vlan_id: 1000
    version: 2

- name: Revert to default query version on VLAN 1000
  jaydee_io.dlink_dgs1250.igmp_snooping_query_version:
    vlan_id: 1000
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
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(vlan_id, version, state):
    if state == "absent":
        return ["vlan %d" % vlan_id, "no ip igmp snooping query-version", "exit"]
    return ["vlan %d" % vlan_id, "ip igmp snooping query-version %d" % version, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            vlan_id=dict(type="int", required=True),
            version=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["version"])],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["vlan_id"],
        module.params["version"],
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
