#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: mgmt_access_class
short_description: Restrict access via a line with an IP ACL on a D-Link DGS-1250 switch
description:
  - Configures the C(access-class) CLI command on a D-Link DGS-1250 switch.
  - Applies or removes a standard IP access list to restrict access via a line (console, telnet, ssh).
  - Corresponds to CLI command described in chapter 5-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.4.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  line:
    description:
      - Line type to configure.
    type: str
    required: true
    choices: [console, telnet, ssh]
  acl_name:
    description:
      - Name of the standard IP access list.
    type: str
    required: true
  state:
    description:
      - C(present) to apply the access class, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command requires Line Configuration Mode.
"""

EXAMPLES = r"""
- name: Restrict Telnet access with ACL 'vty-filter'
  jaydee_io.dlink_dgs1250.mgmt_access_class:
    line: telnet
    acl_name: vty-filter

- name: Remove ACL restriction on Telnet
  jaydee_io.dlink_dgs1250.mgmt_access_class:
    line: telnet
    acl_name: vty-filter
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


def _build_commands(line, acl_name, state):
    prefix = "" if state == "present" else "no "
    return ["line %s" % line, "%saccess-class %s" % (prefix, acl_name), "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            line=dict(type="str", required=True, choices=[
                      "console", "telnet", "ssh"]),
            acl_name=dict(type="str", required=True),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["line"], module.params["acl_name"], module.params["state"])

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
