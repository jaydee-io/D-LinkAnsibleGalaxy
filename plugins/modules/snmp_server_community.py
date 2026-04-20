#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: snmp_server_community
short_description: Configure SNMP community string on a D-Link DGS-1250 switch
description:
  - Configures the C(snmp-server community) CLI command on a D-Link DGS-1250 switch.
  - Creates or removes an SNMP community string.
  - Corresponds to CLI command described in chapter 60-16 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  community:
    description:
      - The community string (max 32 alphanumeric characters).
    type: str
    required: true
  view:
    description:
      - View name to associate with the community.
    type: str
  access_type:
    description:
      - Access type for the community.
    type: str
    choices: [ro, rw]
  access_list:
    description:
      - Standard IP access list name for access control.
    type: str
  state:
    description:
      - C(present) to create, C(absent) to remove.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Create community with read-write and view
  jaydee_io.dlink_dgs1250.snmp_server_community:
    community: comaccess
    view: interfacesMibView
    access_type: rw

- name: Remove community
  jaydee_io.dlink_dgs1250.snmp_server_community:
    community: comaccess
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


def _build_commands(community, view, access_type, access_list, state):
    if state == "absent":
        return ["no snmp-server community %s" % community]
    cmd = "snmp-server community %s" % community
    if view:
        cmd += " view %s" % view
    if access_type:
        cmd += " %s" % access_type
    if access_list:
        cmd += " access %s" % access_list
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            community=dict(type="str", required=True),
            view=dict(type="str"),
            access_type=dict(type="str", choices=["ro", "rw"]),
            access_list=dict(type="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["community"], module.params["view"],
                               module.params["access_type"], module.params["access_list"], module.params["state"])
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
