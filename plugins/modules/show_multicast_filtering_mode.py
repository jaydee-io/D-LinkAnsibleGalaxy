#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: show_multicast_filtering_mode
short_description: Display multicast filtering mode on a D-Link DGS-1250 switch
description:
  - Executes the C(show multicast filtering-mode) CLI command on a D-Link DGS-1250 switch.
  - Displays the filtering mode for handling multicast packets received on a VLAN.
  - Corresponds to CLI command described in chapter 28-11 of the DGS-1250 CLI Reference Guide.
version_added: "0.11.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  vlan_id:
    description:
      - Optional VLAN ID to display multicast filtering mode for.
      - If not specified, all VLANs are displayed.
    type: int
notes:
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display multicast filtering mode for all VLANs
  jaydee_io.dlink_dgs1250.show_multicast_filtering_mode:
  register: result

- name: Display multicast filtering mode for VLAN 100
  jaydee_io.dlink_dgs1250.show_multicast_filtering_mode:
    vlan_id: 100
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


def _build_command(vlan_id):
    if vlan_id is not None:
        return "show multicast filtering-mode interface %d" % vlan_id
    return "show multicast filtering-mode"


def main():
    module = AnsibleModule(
        argument_spec=dict(
            vlan_id=dict(type="int"),
        ),
        supports_check_mode=True,
    )
    command = _build_command(module.params["vlan_id"])
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
