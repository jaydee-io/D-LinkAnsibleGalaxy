#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: acl_list_remark
short_description: Add or remove a remark on an ACL on a D-Link DGS-1250 switch
description:
  - Configures the C(list-remark) CLI command on a D-Link DGS-1250 switch.
  - Adds a text remark to an existing IP, IPv6, or MAC access list.
  - Use C(state=absent) to remove the remark.
  - Corresponds to CLI command described in chapter 4-8 of the DGS-1250 CLI Reference Guide.
version_added: "0.3.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  acl_type:
    description:
      - Type of access list.
    type: str
    required: true
    choices: [ip, ip_extended, ipv6, ipv6_extended, mac]
  acl_name:
    description:
      - Name of the access list to add the remark to.
    type: str
    required: true
  remark:
    description:
      - Remark text (up to 256 characters). Required when C(state=present).
    type: str
  state:
    description:
      - C(present) to add the remark, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command requires entering the ACL Configuration Mode first.
"""

EXAMPLES = r"""
- name: Add remark to extended IP access list
  jaydee_io.dlink_dgs1250.acl_list_remark:
    acl_type: ip_extended
    acl_name: R&D
    remark: "This access-list is used to match any IP packets from the host 10.2.2.1."

- name: Remove remark from access list
  jaydee_io.dlink_dgs1250.acl_list_remark:
    acl_type: ip_extended
    acl_name: R&D
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


_ACL_ENTER = {
    "ip": "ip access-list",
    "ip_extended": "ip access-list extended",
    "ipv6": "ipv6 access-list",
    "ipv6_extended": "ipv6 access-list extended",
    "mac": "mac access-list extended",
}


def _build_commands(acl_type, acl_name, remark, state):
    enter_cmd = "%s %s" % (_ACL_ENTER[acl_type], acl_name)
    cmds = [enter_cmd]
    if state == "present":
        cmds.append("list-remark %s" % remark)
    else:
        cmds.append("no list-remark")
    cmds.append("exit")
    return cmds


def main():
    module = AnsibleModule(
        argument_spec=dict(
            acl_type=dict(type="str", required=True,
                          choices=["ip", "ip_extended", "ipv6", "ipv6_extended", "mac"]),
            acl_name=dict(type="str", required=True),
            remark=dict(type="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["remark"]),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["acl_type"],
        module.params["acl_name"],
        module.params["remark"],
        module.params["state"],
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
