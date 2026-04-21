#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: mstp_max_hops
short_description: Configure MSTP maximum hop count on a D-Link DGS-1250 switch
description:
  - Configures the C(spanning-tree mst max-hops) CLI command on a D-Link DGS-1250 switch.
  - Sets or resets the MSTP maximum hop count value.
  - Corresponds to CLI command described in chapter 46-7 of the DGS-1250 CLI Reference Guide.
version_added: "0.15.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  hop_count:
    description:
      - The maximum hop count (6 to 40). Required when C(state=present).
    type: int
  state:
    description:
      - C(present) to set the value, C(absent) to revert to default (20).
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set MSTP maximum hop count
  jaydee_io.dlink_dgs1250.mstp_max_hops:
    hop_count: 19

- name: Revert MSTP maximum hop count to default
  jaydee_io.dlink_dgs1250.mstp_max_hops:
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


def _build_commands(hop_count, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["no spanning-tree mst max-hops"]
    return ["spanning-tree mst max-hops %d" % hop_count]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            hop_count=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["hop_count"]),
        ],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["hop_count"],
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
