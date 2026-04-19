#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: acl_mac_access_group
short_description: Apply or remove a MAC access list on an interface on a D-Link DGS-1250 switch
description:
  - Configures the C(mac access-group) CLI command on a D-Link DGS-1250 switch.
  - Applies a MAC access list to an interface for ingress filtering of non-IP packets.
  - Use C(state=absent) to remove the access group from the interface.
  - Corresponds to CLI command described in chapter 4-9 of the DGS-1250 CLI Reference Guide.
version_added: "0.3.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Physical port interface (e.g. C(eth1/0/4)).
    type: str
    required: true
  name:
    description:
      - Name or number of the MAC access list to apply.
    type: str
    required: true
  state:
    description:
      - C(present) to apply the access group, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command requires Interface Configuration Mode.
  - MAC access groups only check non-IP packets.
"""

EXAMPLES = r"""
- name: Apply MAC access list 'daily-profile' to port 4
  jaydee_io.dlink_dgs1250.acl_mac_access_group:
    interface: eth1/0/4
    name: daily-profile

- name: Remove MAC access group from port 4
  jaydee_io.dlink_dgs1250.acl_mac_access_group:
    interface: eth1/0/4
    name: daily-profile
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


def _build_commands(interface, name, state):
    cmds = ["interface %s" % interface]
    prefix = "" if state == "present" else "no "
    cmds.append("%smac access-group %s in" % (prefix, name))
    return cmds


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            name=dict(type="str", required=True),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["interface"], module.params["name"], module.params["state"]
    )

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
