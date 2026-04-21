#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jerome Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: mld_snooping_query_version
short_description: Configure MLD snooping query version on a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 mld snooping query-version) CLI command on a D-Link DGS-1250 switch.
  - Corresponds to CLI command described in chapter 45-9 of the DGS-1250 CLI Reference Guide.
version_added: "0.14.0"
author:
  - "Jérôme Dumesnil (@jaydee-io)"
options:
  vlan_id:
    description:
      - The VLAN ID to configure.
    type: int
    required: true
  version:
    description:
      - The query version (1 or 2).
    type: int
  state:
    description:
      - C(present) to set the value, C(absent) to revert to default (2).
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in VLAN Configuration Mode.
"""

EXAMPLES = r"""
- name: Set ipv6 mld snooping query-version on VLAN 1000
  jaydee_io.dlink_dgs1250.mld_snooping_query_version:
    vlan_id: 1000
    version: 1

- name: Revert ipv6 mld snooping query-version to default on VLAN 1000
  jaydee_io.dlink_dgs1250.mld_snooping_query_version:
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
        run_commands, is_config_present, build_config_diff, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, is_config_present, build_config_diff, MODE_GLOBAL_CONFIG


def _build_commands(vlan_id, version, state):
    if state == "absent":
        return ["vlan %d" % vlan_id, "no ipv6 mld snooping query-version", "exit"]
    return ["vlan %d" % vlan_id, "ipv6 mld snooping query-version %d" % version, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            vlan_id=dict(type="int", required=True),
            version=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["version"]),
        ],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["vlan_id"], module.params["version"], module.params["state"])
    if is_config_present(module, commands):
        module.exit_json(changed=False, commands=[], raw_output="")
        return
    diff = build_config_diff(module, commands) if module._diff else None
    if module.check_mode:
        result = dict(changed=True, commands=commands, raw_output="")
        if diff:
            result['diff'] = diff
        module.exit_json(**result)
        return
    try:
        raw_output = run_commands(module, commands, mode=MODE_GLOBAL_CONFIG)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    result = dict(changed=True, raw_output=raw_output, commands=commands)
    if diff:
        result['diff'] = diff
    module.exit_json(**result)


if __name__ == "__main__":
    main()
