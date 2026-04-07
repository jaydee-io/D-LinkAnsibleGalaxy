#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: acl_ip_access_group
short_description: Apply or remove an IP access list on an interface on a D-Link DGS-1250 switch
description:
  - Configures the C(ip access-group) CLI command on a D-Link DGS-1250 switch.
  - Applies an IP access list to an interface for ingress filtering.
  - Use C(state=absent) to remove the access group from the interface.
  - Corresponds to CLI command described in chapter 4-4 of the DGS-1250 CLI Reference Guide.
version_added: "0.3.0"
author:
  - Jérôme Dumesnil
options:
  interface:
    description:
      - Physical port interface (e.g. C(eth1/0/2)).
    type: str
    required: true
  name:
    description:
      - Name or number of the IP access list to apply.
    type: str
    required: true
  state:
    description:
      - C(present) to apply the access group, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This module requires C(ansible_network_os=dlink.dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command requires Interface Configuration Mode.
  - Only one IP access list can be applied per interface; a new one overwrites the previous.
"""

EXAMPLES = r"""
- name: Apply IP access list 'Strict-Control' to port 2
  dlink.dgs1250.acl_ip_access_group:
    interface: eth1/0/2
    name: Strict-Control

- name: Remove IP access group from port 2
  dlink.dgs1250.acl_ip_access_group:
    interface: eth1/0/2
    name: Strict-Control
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
    from ansible_collections.dlink.dgs1250.plugins.module_utils.dgs1250 import (
        run_commands, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(interface, name, state):
    cmds = ["interface %s" % interface]
    prefix = "" if state == "present" else "no "
    cmds.append("%sip access-group %s in" % (prefix, name))
    return cmds


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            name=dict(type="str", required=True),
            state=dict(type="str", choices=["present", "absent"], default="present"),
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
