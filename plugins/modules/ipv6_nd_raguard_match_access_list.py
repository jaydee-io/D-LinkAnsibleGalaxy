#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: ipv6_nd_raguard_match_access_list
short_description: Filter RA messages by IPv6 access list in an RA guard policy on a D-Link DGS-1250 switch
description:
  - Configures the C(match ipv6 access-list) CLI command inside an RA guard policy on a D-Link DGS-1250 switch.
  - Filters RA messages based on the sender IPv6 address using an access list.
  - Corresponds to CLI command described in chapter 56-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  policy:
    description:
      - The RA guard policy name.
    type: str
    required: true
  access_list:
    description:
      - Standard IPv6 access list name. Required when C(state=present).
    type: str
  state:
    description:
      - C(present) to set the access list filter, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in RA Guard Policy Configuration Mode.
"""

EXAMPLES = r"""
- name: Filter RA messages by access list
  jaydee_io.dlink_dgs1250.ipv6_nd_raguard_match_access_list:
    policy: raguard1
    access_list: list1

- name: Remove access list filter
  jaydee_io.dlink_dgs1250.ipv6_nd_raguard_match_access_list:
    policy: raguard1
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


def _build_commands(policy, access_list, state):
    commands = ["ipv6 nd raguard policy %s" % policy]
    if state == "absent":
        commands.append("no match ipv6 access-list")
    else:
        commands.append("match ipv6 access-list %s" % access_list)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy=dict(type="str", required=True),
            access_list=dict(type="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["access_list"])],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["policy"], module.params["access_list"], module.params["state"])
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
