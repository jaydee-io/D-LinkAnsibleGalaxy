#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: ipv6_source_guard_policy
short_description: Create or delete an IPv6 source guard policy on a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 source-guard policy) CLI command on a D-Link DGS-1250 switch.
  - Creates or removes an IPv6 source guard policy.
  - Corresponds to CLI command described in chapter 38-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.13.0"
author:
  - Jérôme Dumesnil
options:
  policy:
    description:
      - Name of the source guard policy.
    type: str
    required: true
  state:
    description:
      - C(present) to create the policy, C(absent) to delete it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Create an IPv6 source guard policy
  jaydee_io.dlink_dgs1250.ipv6_source_guard_policy:
    policy: policy1

- name: Delete an IPv6 source guard policy
  jaydee_io.dlink_dgs1250.ipv6_source_guard_policy:
    policy: policy1
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


def _build_commands(policy, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["no ipv6 source-guard policy %s" % policy]
    return ["ipv6 source-guard policy %s" % policy]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy=dict(type="str", required=True),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["policy"],
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
