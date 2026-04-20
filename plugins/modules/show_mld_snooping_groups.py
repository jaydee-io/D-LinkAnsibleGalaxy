#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jerome Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: show_mld_snooping_groups
short_description: Display MLD snooping group information on a D-Link DGS-1250 switch
description:
  - Executes the C(show ipv6 mld snooping groups) CLI command on a D-Link DGS-1250 switch.
  - Displays MLD snooping group-related information.
  - Corresponds to CLI command described in chapter 45-14 of the DGS-1250 CLI Reference Guide.
version_added: "0.14.0"
author:
  - "Jérôme Dumesnil (@jaydee-io)"
options:
  group_address:
    description:
      - Optional IPv6 group address to filter.
    type: str
  vlan_id:
    description:
      - Optional VLAN ID to filter.
    type: int
notes:
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display all MLD snooping groups
  jaydee_io.dlink_dgs1250.show_mld_snooping_groups:
  register: result

- name: Display MLD snooping groups for a VLAN
  jaydee_io.dlink_dgs1250.show_mld_snooping_groups:
    vlan_id: 1
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
    if group_address:
        return "show ipv6 mld snooping groups %s" % group_address
    if vlan_id:
        return "show ipv6 mld snooping groups vlan %d" % vlan_id
    return "show ipv6 mld snooping groups"


def main():
    module = AnsibleModule(
        argument_spec=dict(
            group_address=dict(type="str"),
            vlan_id=dict(type="int"),
        ),
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
