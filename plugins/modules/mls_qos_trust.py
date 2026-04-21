#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: mls_qos_trust
short_description: Configure the trust state of an interface on a D-Link DGS-1250 switch
description:
  - Configures the C(mls qos trust) CLI command on a D-Link DGS-1250 switch.
  - Sets the port to trust CoS or DSCP fields of arriving packets.
  - Corresponds to CLI command described in chapter 54-9 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/1)).
    type: str
    required: true
  trust:
    description:
      - Field to trust for QoS operations.
    type: str
    choices: [cos, dscp]
  state:
    description:
      - C(present) to configure trust, C(absent) to revert to default (trust CoS).
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Trust DSCP on eth1/0/1
  jaydee_io.dlink_dgs1250.mls_qos_trust:
    interface: eth1/0/1
    trust: dscp

- name: Revert to default trust
  jaydee_io.dlink_dgs1250.mls_qos_trust:
    interface: eth1/0/1
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


def _build_commands(interface, trust, state):
    commands = ["interface %s" % interface]
    if state == "absent":
        commands.append("no mls qos trust")
    else:
        commands.append("mls qos trust %s" % trust)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            trust=dict(type="str", choices=["cos", "dscp"]),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["trust"])],
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interface"],
        module.params["trust"],
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
