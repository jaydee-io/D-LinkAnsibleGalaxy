#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: voice_vlan_qos
short_description: Configure voice VLAN CoS priority on a D-Link DGS-1250 switch
description:
  - Configures the C(voice vlan qos) CLI command on a D-Link DGS-1250 switch.
  - Sets the CoS priority for incoming voice VLAN traffic.
  - Corresponds to CLI command described in chapter 71-6 of the DGS-1250 CLI Reference Guide.
version_added: "0.19.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  cos_value:
    description:
      - The CoS priority value (0 to 7).
    type: int
  state:
    description:
      - C(present) to set, C(absent) to revert to default (5).
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set voice VLAN CoS to 7
  jaydee_io.dlink_dgs1250.voice_vlan_qos:
    cos_value: 7

- name: Revert to default
  jaydee_io.dlink_dgs1250.voice_vlan_qos:
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
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(cos_value, state):
    if state == "absent":
        return ["no voice vlan qos"]
    return ["voice vlan qos %d" % cos_value]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            cos_value=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["cos_value"], module.params["state"])
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
