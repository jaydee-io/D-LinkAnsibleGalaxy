#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: rmon_collection_stats
short_description: Enable RMON statistics collection on an interface of a D-Link DGS-1250 switch
description:
  - Configures the C(rmon collection stats) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables RMON statistics on a configured interface.
  - Corresponds to CLI command described in chapter 55-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/2)).
    type: str
    required: true
  index:
    description:
      - RMON table index (1-65535).
    type: int
    required: true
  owner:
    description:
      - Owner string (max 127 characters).
    type: str
  state:
    description:
      - C(present) to enable statistics, C(absent) to disable.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable RMON stats index 65 owned by guest on eth1/0/2
  jaydee_io.dlink_dgs1250.rmon_collection_stats:
    interface: eth1/0/2
    index: 65
    owner: guest

- name: Disable RMON stats index 65
  jaydee_io.dlink_dgs1250.rmon_collection_stats:
    interface: eth1/0/2
    index: 65
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


def _build_commands(interface, index, owner, state):
    commands = ["interface %s" % interface]
    if state == "absent":
        commands.append("no rmon collection stats %d" % index)
    else:
        cmd = "rmon collection stats %d" % index
        if owner:
            cmd += " owner %s" % owner
        commands.append(cmd)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            index=dict(type="int", required=True),
            owner=dict(type="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interface"],
        module.params["index"],
        module.params["owner"],
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
