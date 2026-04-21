#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: surveillance_vlan_onvif_nvr_description
short_description: Configure ONVIF NVR description on a D-Link DGS-1250 switch
description:
  - Configures the C(surveillance vlan onvif-nvr) description CLI command on a D-Link DGS-1250 switch.
  - Sets or removes the description for an ONVIF recognized NVR.
  - Corresponds to CLI command described in chapter 63-8 of the DGS-1250 CLI Reference Guide.
version_added: "0.18.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  ip_address:
    description:
      - The IP address of the NVR.
    type: str
    required: true
  mac_address:
    description:
      - The MAC address of the NVR.
    type: str
  description:
    description:
      - Description text (max 32 characters).
    type: str
  state:
    description:
      - C(present) to set, C(absent) to remove.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set NVR description
  jaydee_io.dlink_dgs1250.surveillance_vlan_onvif_nvr_description:
    ip_address: 172.18.60.2
    description: nvr1

- name: Remove NVR description
  jaydee_io.dlink_dgs1250.surveillance_vlan_onvif_nvr_description:
    ip_address: 172.18.60.2
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


def _build_commands(ip_address, mac_address, description, state):
    cmd = "surveillance vlan onvif-nvr %s" % ip_address
    if mac_address is not None:
        cmd += " mac-address %s" % mac_address
    if state == "absent":
        return ["no " + cmd + " description"]
    cmd += " description %s" % description
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            ip_address=dict(type="str", required=True),
            mac_address=dict(type="str"),
            description=dict(type="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["ip_address"], module.params["mac_address"], module.params["description"], module.params["state"])
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
