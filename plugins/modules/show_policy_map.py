#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: show_policy_map
short_description: Display the policy-map configuration on a D-Link DGS-1250 switch
description:
  - Displays the output of the C(show policy-map) CLI command.
  - Corresponds to CLI command described in chapter 54-20 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  policy_name:
    description:
      - Optional name of a policy map to display (mutually exclusive with C(interface)).
    type: str
  interface:
    description:
      - Optional interface whose attached policy map to display (mutually exclusive with C(policy_name)).
    type: str
notes:
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Show all policy maps
  jaydee_io.dlink_dgs1250.show_policy_map:

- name: Show policy map policy1
  jaydee_io.dlink_dgs1250.show_policy_map:
    policy_name: policy1

- name: Show policy attached to eth1/0/1
  jaydee_io.dlink_dgs1250.show_policy_map:
    interface: eth1/0/1
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
        run_command,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _build_command(policy_name, interface):
    cmd = "show policy-map"
    if policy_name:
        cmd += " %s" % policy_name
    elif interface:
        cmd += " interface %s" % interface
    return cmd


def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy_name=dict(type="str"),
            interface=dict(type="str"),
        ),
        mutually_exclusive=[("policy_name", "interface")],
        supports_check_mode=True,
    )
    command = _build_command(
        module.params["policy_name"],
        module.params["interface"],
    )
    if module.check_mode:
        module.exit_json(changed=False, commands=[command], raw_output="")
        return
    try:
        raw_output = run_command(module, command)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    module.exit_json(changed=False, raw_output=raw_output, commands=[command])


if __name__ == "__main__":
    main()
