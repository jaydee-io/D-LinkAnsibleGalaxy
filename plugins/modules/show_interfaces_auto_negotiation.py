#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: show_interfaces_auto_negotiation
short_description: Display interface auto-negotiation information on a D-Link DGS-1250 switch
description:
  - Executes the C(show interfaces auto-negotiation) CLI command on a D-Link DGS-1250 switch.
  - Displays detailed auto-negotiation information of physical port interfaces.
  - Corresponds to CLI command described in chapter 30-10 of the DGS-1250 CLI Reference Guide.
version_added: "0.11.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface_id:
    description:
      - Optional interface(s) to display auto-negotiation for (e.g. C(eth1/0/1-2)).
      - If not specified, all physical port interfaces are displayed.
    type: str
notes:
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display auto-negotiation information for all ports
  jaydee_io.dlink_dgs1250.show_interfaces_auto_negotiation:
  register: result

- name: Display auto-negotiation information for ports 1 to 2
  jaydee_io.dlink_dgs1250.show_interfaces_auto_negotiation:
    interface_id: eth1/0/1-2
  register: result
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


def _build_command(interface_id):
    if interface_id:
        return "show interfaces %s auto-negotiation" % interface_id
    return "show interfaces auto-negotiation"


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface_id=dict(type="str"),
        ),
        supports_check_mode=True,
    )
    command = _build_command(module.params["interface_id"])
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
