#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: acl_ip_access_list
short_description: Create or delete an IP access list on a D-Link DGS-1250 switch
description:
  - Configures the C(ip access-list) CLI command on a D-Link DGS-1250 switch.
  - Creates a standard or extended IP access list.
  - Use C(state=absent) to delete the access list.
  - Corresponds to CLI command described in chapter 4-5 of the DGS-1250 CLI Reference Guide.
version_added: "0.3.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  name:
    description:
      - Name of the IP access list. Maximum 32 characters, first character must be a letter.
    type: str
    required: true
  number:
    description:
      - ID number of the IP access list.
      - Standard IP access lists use 1-1999, extended use 2000-3999.
      - If omitted, the switch assigns the next available number.
    type: int
  extended:
    description:
      - Whether this is an extended IP access list.
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
  - Creating the access list enters ACL Config Mode on the switch. The module sends C(exit) to return.
"""

EXAMPLES = r"""
- name: Create an extended IP access list named 'Strict-Control'
  jaydee_io.dlink_dgs1250.acl_ip_access_list:
    name: Strict-Control
    extended: true

- name: Create a standard IP access list named 'pim-srcfilter'
  jaydee_io.dlink_dgs1250.acl_ip_access_list:
    name: pim-srcfilter

- name: Delete IP access list 'Strict-Control'
  jaydee_io.dlink_dgs1250.acl_ip_access_list:
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
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import (
        run_commands, is_config_present, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, is_config_present, MODE_GLOBAL_CONFIG


def _build_commands(name, number, extended, state):
    prefix = "" if state == "present" else "no "
    ext = " extended" if extended else ""
    cmd = "%sip access-list%s %s" % (prefix, ext, name)
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
