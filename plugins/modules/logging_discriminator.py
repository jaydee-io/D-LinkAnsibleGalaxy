#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: logging_discriminator
short_description: Configure a logging discriminator on a D-Link DGS-1250 switch
description:
  - Configures the C(logging discriminator) CLI command on a D-Link DGS-1250 switch.
  - Creates or removes a discriminator to filter SYSLOG messages.
  - Corresponds to CLI command described in chapter 66-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.19.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  name:
    description:
      - Name of the discriminator.
    type: str
    required: true
  facility_match:
    description:
      - Whether to include or drop matching facility strings.
    type: str
    choices: [includes, drops]
  facility_string:
    description:
      - Facility name(s) to filter (comma-separated, no spaces).
    type: str
  severity_match:
    description:
      - Whether to include or drop matching severity levels.
    type: str
    choices: [includes, drops]
  severity_list:
    description:
      - List of severity levels to filter (comma-separated).
    type: str
  state:
    description:
      - C(present) to create, C(absent) to remove.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Create discriminator with facility and severity filter
  jaydee_io.dlink_dgs1250.logging_discriminator:
    name: buffer-filter
    facility_match: includes
    facility_string: STP
    severity_match: includes
    severity_list: "14,6"

- name: Remove discriminator
  jaydee_io.dlink_dgs1250.logging_discriminator:
    name: buffer-filter
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


def _build_commands(name, facility_match, facility_string, severity_match, severity_list, state):
    if state == "absent":
        return ["no logging discriminator %s" % name]
    cmd = "logging discriminator %s" % name
    if facility_match is not None and facility_string is not None:
        cmd += " facility %s %s" % (facility_match, facility_string)
    if severity_match is not None and severity_list is not None:
        cmd += " severity %s %s" % (severity_match, severity_list)
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type="str", required=True),
            facility_match=dict(type="str", choices=["includes", "drops"]),
            facility_string=dict(type="str"),
            severity_match=dict(type="str", choices=["includes", "drops"]),
            severity_list=dict(type="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["name"], module.params["facility_match"], module.params["facility_string"],
                               module.params["severity_match"], module.params["severity_list"], module.params["state"])
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
