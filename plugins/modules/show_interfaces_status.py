#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: show_interfaces_status
short_description: Display interface connection status on a D-Link DGS-1250 switch
description:
  - Executes the C(show interfaces status) CLI command on a D-Link DGS-1250 switch.
  - Displays the port connection status of the Switch.
  - Returns both raw text output and a structured C(parsed) list.
  - Corresponds to CLI command described in chapter 30-8 of the DGS-1250 CLI Reference Guide.
version_added: "0.11.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface_id:
    description:
      - Optional interface(s) to display status for (e.g. C(eth1/0/1-8)).
      - If not specified, status of all switch ports is displayed.
    type: str
notes:
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display status of all switch ports
  jaydee_io.dlink_dgs1250.show_interfaces_status:
  register: result

- name: Display status of ports 1 to 8
  jaydee_io.dlink_dgs1250.show_interfaces_status:
    interface_id: eth1/0/1-8
  register: result

- name: Find connected ports
  jaydee_io.dlink_dgs1250.show_interfaces_status:
  register: result

- name: Show connected ports
  ansible.builtin.debug:
    msg: "{{ item.port }} is up at {{ item.speed }}"
  loop: "{{ result.parsed | selectattr('status', 'equalto', 'connected') }}"
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
parsed:
  description: Structured list of interface status entries parsed from the CLI output.
  returned: always
  type: list
  elements: dict
  contains:
    port:
      description: Interface name.
      type: str
    status:
      description: Link status (connected, not-connected, disabled).
      type: str
    vlan:
      description: Access VLAN ID.
      type: str
    duplex:
      description: Duplex mode (auto, full, half).
      type: str
    speed:
      description: Port speed (auto, 10M, 100M, 1000M, 10G).
      type: str
    type:
      description: Port media type (1000BASE-T, 10GBASE-SR, etc.).
      type: str
"""

from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import (
        run_command,
    )
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250_parsers import (
        parse_interfaces,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command
    from dgs1250_parsers import parse_interfaces


def _build_command(interface_id):
    if interface_id:
        return "show interfaces %s status" % interface_id
    return "show interfaces status"


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface_id=dict(type="str"),
        ),
        supports_check_mode=True,
    )
    command = _build_command(module.params["interface_id"])
    if module.check_mode:
        module.exit_json(changed=False, commands=[command], raw_output="",
                         parsed=[])
        return
    try:
        raw_output = run_command(module, command)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    module.exit_json(changed=False, raw_output=raw_output, commands=[command],
                     parsed=parse_interfaces(raw_output))


if __name__ == "__main__":
    main()
