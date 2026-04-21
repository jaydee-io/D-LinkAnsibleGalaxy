#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: rmon_event
short_description: Configure an RMON event entry on a D-Link DGS-1250 switch
description:
  - Configures the C(rmon event) CLI command on a D-Link DGS-1250 switch.
  - Creates or removes an RMON event entry.
  - Corresponds to CLI command described in chapter 55-4 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  index:
    description:
      - Event index (1-65535).
    type: int
    required: true
  log:
    description:
      - Generate log message for the notification.
    type: bool
    default: false
  trap_community:
    description:
      - Generate SNMP trap to the specified community (max 127 characters).
    type: str
  owner:
    description:
      - Owner string (max 127 characters).
    type: str
  description:
    description:
      - Description for the event entry (max 127 characters).
    type: str
  state:
    description:
      - C(present) to create the event, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Create RMON event with log
  jaydee_io.dlink_dgs1250.rmon_event:
    index: 13
    log: true
    owner: "it@domain.com"
    description: "ifInNUcastPkts is too much"

- name: Remove RMON event
  jaydee_io.dlink_dgs1250.rmon_event:
    index: 13
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


def _build_commands(index, log, trap_community, owner, description, state):
    if state == "absent":
        return ["no rmon event %d" % index]
    cmd = "rmon event %d" % index
    if log:
        cmd += " log"
    if trap_community:
        cmd += " trap %s" % trap_community
    if owner:
        cmd += " owner %s" % owner
    if description:
        cmd += " description %s" % description
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            index=dict(type="int", required=True),
            log=dict(type="bool", default=False),
            trap_community=dict(type="str"),
            owner=dict(type="str"),
            description=dict(type="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    p = module.params
    commands = _build_commands(
        p["index"], p["log"], p["trap_community"],
        p["owner"], p["description"], p["state"],
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
