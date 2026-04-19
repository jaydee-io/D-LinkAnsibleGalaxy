#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: show_cpu_protect_type
short_description: Display CPU protect type settings on a D-Link DGS-1250 switch
description:
  - Executes the C(show cpu-protect type) CLI command on a D-Link DGS-1250 switch.
  - Displays the rate limit and statistics for a specified protocol.
  - Corresponds to CLI command described in chapter 57-7 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  protocol_name:
    description:
      - The protocol name to display.
    type: str
    required: true
notes:
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Show ARP protocol rate limit
  jaydee_io.dlink_dgs1250.show_cpu_protect_type:
    protocol_name: arp
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
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _build_command(protocol_name):
    return "show cpu-protect type %s" % protocol_name


def main():
    module = AnsibleModule(
        argument_spec=dict(
            protocol_name=dict(type="str", required=True),
        ),
        supports_check_mode=True,
    )
    command = _build_command(module.params["protocol_name"])
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
