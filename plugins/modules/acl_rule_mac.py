#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: acl_rule_mac
short_description: Add or remove a permit/deny rule in a MAC access list on a D-Link DGS-1250 switch
description:
  - Sends a permit or deny rule inside a MAC access list on a D-Link DGS-1250 switch.
  - The rule is passed as a raw CLI string to support the full syntax (MAC addresses,
    wildcards, ethernet-type, cos, vlan, time-range).
  - Use C(state=absent) with C(sequence) to remove a specific rule.
  - Corresponds to CLI command described in chapter 4-13 of the DGS-1250 CLI Reference Guide.
version_added: "0.3.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  acl_name:
    description:
      - Name of the MAC access list.
    type: str
    required: true
  rule:
    description:
      - The full permit/deny rule string
        (e.g. C(permit 00:80:33:00:00:00 00:00:00:ff:ff:ff any)).
      - Required when C(state=present).
    type: str
  sequence:
    description:
      - Sequence number of the rule to delete. Required when C(state=absent).
    type: int
  state:
    description:
      - C(present) to add the rule, C(absent) to remove it by sequence number.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command requires entering the MAC Access-list Configuration Mode.
  - MAC access lists are always extended on the DGS-1250.
"""

EXAMPLES = r"""
- name: Add permit rule for specific source MAC
  jaydee_io.dlink_dgs1250.acl_rule_mac:
    acl_name: daily-profile
    rule: "permit 00:80:33:00:00:00 00:00:00:ff:ff:ff any"

- name: Remove rule by sequence number
  jaydee_io.dlink_dgs1250.acl_rule_mac:
    acl_name: daily-profile
    sequence: 10
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
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(acl_name, rule, sequence, state):
    enter_cmd = "mac access-list extended %s" % acl_name
    cmds = [enter_cmd]
    if state == "present":
        cmds.append(rule)
    else:
        cmds.append("no %d" % sequence)
    cmds.append("exit")
    return cmds


def main():
    module = AnsibleModule(
        argument_spec=dict(
            acl_name=dict(type="str", required=True),
            rule=dict(type="str"),
            sequence=dict(type="int"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["rule"]),
            ("state", "absent", ["sequence"]),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["acl_name"],
        module.params["rule"],
        module.params["sequence"],
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
