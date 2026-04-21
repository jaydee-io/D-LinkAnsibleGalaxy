#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: acl_ipv6_access_list
short_description: Create or delete an IPv6 access list on a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 access-list) CLI command on a D-Link DGS-1250 switch.
  - Creates a standard or extended IPv6 access list.
  - Use C(state=absent) to delete the access list.
  - Corresponds to CLI command described in chapter 4-7 of the DGS-1250 CLI Reference Guide.
version_added: "0.3.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  name:
    description:
      - Name of the IPv6 access list. Maximum 32 characters.
    type: str
    required: true
  number:
    description:
      - ID number of the IPv6 access list.
      - Standard IPv6 access lists use 11000-12999, extended use 13000-14999.
      - If omitted, the switch assigns the next available number.
    type: int
  extended:
    description:
      - Whether this is an extended IPv6 access list.
    type: bool
    default: false
  state:
    description:
      - C(present) to create the access list, C(absent) to delete it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command requires Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Create an extended IPv6 access list named 'ip6-control'
  jaydee_io.dlink_dgs1250.acl_ipv6_access_list:
    name: ip6-control
    extended: true

- name: Create a standard IPv6 access list
  jaydee_io.dlink_dgs1250.acl_ipv6_access_list:
    name: ip6-std-control

- name: Delete IPv6 access list 'ip6-control'
  jaydee_io.dlink_dgs1250.acl_ipv6_access_list:
    name: ip6-control
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
        run_commands, is_config_present, build_config_diff, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, is_config_present, build_config_diff, MODE_GLOBAL_CONFIG


def _build_commands(name, number, extended, state):
    prefix = "" if state == "present" else "no "
    ext = " extended" if extended else ""
    cmd = "%sipv6 access-list%s %s" % (prefix, ext, name)
    if number is not None and state == "present":
        cmd += " %d" % number
    cmds = [cmd]
    if state == "present":
        cmds.append("exit")
    return cmds


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type="str", required=True),
            number=dict(type="int"),
            extended=dict(type="bool", default=False),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["name"],
        module.params["number"],
        module.params["extended"],
        module.params["state"],
    )

    if is_config_present(module, commands):
        module.exit_json(changed=False, commands=[], raw_output="")
        return
    diff = build_config_diff(module, commands) if module._diff else None
    if module.check_mode:
        result = dict(changed=True, commands=commands, raw_output="")
        if diff:
            result['diff'] = diff
        module.exit_json(**result)
        return

    try:
        raw_output = run_commands(module, commands, mode=MODE_GLOBAL_CONFIG)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    result = dict(changed=True, raw_output=raw_output, commands=commands)
    if diff:
        result['diff'] = diff
    module.exit_json(**result)


if __name__ == "__main__":
    main()
