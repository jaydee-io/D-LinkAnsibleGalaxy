#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jerome Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: loopback_detection_vlan
short_description: Configure loopback detection VLANs on a D-Link DGS-1250 switch
description:
  - Configures the C(loopback-detection vlan) CLI command on a D-Link DGS-1250 switch.
  - Configures VLANs to be enabled for loopback detection.
  - Corresponds to CLI command described in chapter 42-4 of the DGS-1250 CLI Reference Guide.
version_added: "0.14.0"
author:
  - "Jérôme Dumesnil (@jaydee-io)"
options:
  vlan_list:
    description:
      - The VLAN list (e.g. C(100-200) or C(1,2,3)).
    type: str
    required: true
  state:
    description:
      - C(present) to enable VLANs for loopback detection, C(absent) to disable them.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable VLANs 100-200 for loopback detection
  jaydee_io.dlink_dgs1250.loopback_detection_vlan:
    vlan_list: "100-200"

- name: Remove VLANs from loopback detection
  jaydee_io.dlink_dgs1250.loopback_detection_vlan:
    vlan_list: "100-200"
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


def _build_commands(vlan_list, state):
    prefix = "no " if state == "absent" else ""
    return ["%sloopback-detection vlan %s" % (prefix, vlan_list)]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            vlan_list=dict(type="str", required=True),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["vlan_list"], module.params["state"])
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
