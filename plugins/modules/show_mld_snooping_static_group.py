#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: show_mld_snooping_static_group
short_description: Display MLD snooping static group information on a D-Link DGS-1250 switch
description:
  - Executes the C(show ipv6 mld snooping static-group) CLI command on a D-Link DGS-1250 switch.
  - Displays statically configured MLD snooping groups on the switch.
  - Corresponds to CLI command described in chapter 45-16 of the DGS-1250 CLI Reference Guide.
version_added: "0.20.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  group_address:
    description:
      - Optional IPv6 multicast group address to filter by.
    type: str
  vlan_id:
    description:
      - Optional VLAN ID to filter by.
    type: int
notes:
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display all MLD snooping static groups
  jaydee_io.dlink_dgs1250.show_mld_snooping_static_group:
  register: result

- name: Display static groups for a specific group address
  jaydee_io.dlink_dgs1250.show_mld_snooping_static_group:
    group_address: "FF02::1:FF00:1"
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


def _build_command(group_address, vlan_id):
    cmd = "show ipv6 mld snooping static-group"
    if group_address:
        cmd += " %s" % group_address
    elif vlan_id:
        cmd += " vlan %d" % vlan_id
    return cmd


def main():
    module = AnsibleModule(
        argument_spec=dict(
            group_address=dict(type="str"),
            vlan_id=dict(type="int"),
        ),
        mutually_exclusive=[("group_address", "vlan_id")],
        supports_check_mode=True,
    )
    command = _build_command(
        module.params["group_address"], module.params["vlan_id"])
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
