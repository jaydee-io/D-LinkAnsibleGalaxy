#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: show_poe_pd_alive
short_description: Display PoE PD alive check settings on a D-Link DGS-1250 switch
description:
  - Executes the C(show poe pd alive) CLI command on a D-Link DGS-1250 switch.
  - Displays the PD alive check settings.
  - Corresponds to CLI command described in chapter 51-12 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Optional interface ID (e.g. C(eth1/0/1), C(eth1/0/1-2)).
    type: str
notes:
  - This command runs in Privileged EXEC Mode.
  - Only applies to DGS-1250-28XMP and DGS-1250-52XMP models.
"""

EXAMPLES = r"""
- name: Show PoE PD alive check settings on all ports
  jaydee_io.dlink_dgs1250.show_poe_pd_alive:
  register: result

- name: Show settings on a specific port
  jaydee_io.dlink_dgs1250.show_poe_pd_alive:
    interface: eth1/0/1
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
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _build_command(interface):
    cmd = "show poe pd alive"
    if interface:
        cmd += " interface %s" % interface
    return cmd


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str"),
        ),
        supports_check_mode=True,
    )
    command = _build_command(module.params["interface"])
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
