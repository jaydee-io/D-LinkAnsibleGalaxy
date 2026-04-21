#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: ipv6_snooping_limit_address_count
short_description: Configure IPv6 snooping binding entry limit on a D-Link DGS-1250 switch
description:
  - Configures the C(limit address-count) CLI command in IPv6 Snooping Configuration Mode on a D-Link DGS-1250 switch.
  - Limits the maximum number of IPv6 snooping binding entries.
  - Corresponds to CLI command described in chapter 37-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.13.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  policy:
    description:
      - Name of the IPv6 snooping policy to configure.
    type: str
    required: true
  maximum:
    description:
      - Maximum number of binding entries (0 to 511). Required when C(state=present).
    type: int
  state:
    description:
      - C(present) to set the limit, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in IPv6 Snooping Configuration Mode.
"""

EXAMPLES = r"""
- name: Set limit address count to 25
  jaydee_io.dlink_dgs1250.ipv6_snooping_limit_address_count:
    policy: policy1
    maximum: 25

- name: Remove limit address count
  jaydee_io.dlink_dgs1250.ipv6_snooping_limit_address_count:
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
        run_commands, is_config_present, build_config_diff, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, is_config_present, build_config_diff, MODE_GLOBAL_CONFIG


def _build_commands(policy, maximum, state):
    """Build the CLI command list."""
    commands = ["ipv6 snooping policy %s" % policy]
    if state == "absent":
        commands.append("no limit address-count")
    else:
        commands.append("limit address-count %d" % maximum)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy=dict(type="str", required=True),
            maximum=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["maximum"]),
        ],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["policy"],
        module.params["maximum"],
        module.params["state"],
    )
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
