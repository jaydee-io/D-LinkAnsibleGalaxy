#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: snmp_server_view
short_description: Create or remove an SNMP view entry on a D-Link DGS-1250 switch
description:
  - Configures the C(snmp-server view) CLI command on a D-Link DGS-1250 switch.
  - Creates or removes a view entry for SNMP MIB objects.
  - Corresponds to CLI command described in chapter 60-21 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  view:
    description:
      - View name (1-32 characters, no spaces).
    type: str
    required: true
  oid_tree:
    description:
      - OID tree (e.g. C(1.3.6.1.2.1.2) or C(system)). Required when C(state=present).
    type: str
  view_type:
    description:
      - Whether the sub-tree is included or excluded. Required when C(state=present).
    type: str
    choices: [included, excluded]
  state:
    description:
      - C(present) to create/modify, C(absent) to remove.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Create MIB view
  jaydee_io.dlink_dgs1250.snmp_server_view:
    view: interfacesMibView
    oid_tree: 1.3.6.1.2.1.2
    view_type: included

- name: Remove view
  jaydee_io.dlink_dgs1250.snmp_server_view:
    view: interfacesMibView
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


def _build_commands(view, oid_tree, view_type, state):
    if state == "absent":
        return ["no snmp-server view %s" % view]
    return ["snmp-server view %s %s %s" % (view, oid_tree, view_type)]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            view=dict(type="str", required=True),
            oid_tree=dict(type="str"),
            view_type=dict(type="str", choices=["included", "excluded"]),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[("state", "present", ["oid_tree", "view_type"])],
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["view"], module.params["oid_tree"],
                               module.params["view_type"], module.params["state"])
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
