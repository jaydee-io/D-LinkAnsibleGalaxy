#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: acl_rule_ipv6
short_description: Add or remove a permit/deny rule in an IPv6 access list on a D-Link DGS-1250 switch
description:
  - Sends a permit or deny rule inside an IPv6 access list on a D-Link DGS-1250 switch.
  - The rule is passed as a raw CLI string to support the full syntax.
  - Use C(state=absent) with C(sequence) to remove a specific rule.
  - Corresponds to CLI command described in chapter 4-12 of the DGS-1250 CLI Reference Guide.
version_added: "0.3.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  acl_name:
    description:
      - Name of the IPv6 access list.
    type: str
    required: true
  extended:
    description:
      - Whether this is an extended IPv6 access list.
    type: bool
    default: false
  rule:
    description:
      - The full permit/deny rule string (e.g. C(permit tcp any ff02::0:2/16)).
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
  - This command requires entering the IPv6 Access-list Configuration Mode.
"""

EXAMPLES = r"""
- name: Add permit rule for TCP to IPv6 network
  jaydee_io.dlink_dgs1250.acl_rule_ipv6:
    acl_name: ipv6-control
    extended: true
    rule: "permit tcp any ff02::0:2/16"

- name: Remove rule by sequence number
  jaydee_io.dlink_dgs1250.acl_rule_ipv6:
    acl_name: ipv6-control
    extended: true
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
        run_commands, is_config_present, build_config_diff, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, is_config_present, build_config_diff, MODE_GLOBAL_CONFIG


def _build_commands(acl_name, extended, rule, sequence, state):
    ext = " extended" if extended else ""
    enter_cmd = "ipv6 access-list%s %s" % (ext, acl_name)
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
            extended=dict(type="bool", default=False),
            rule=dict(type="str"),
            sequence=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["rule"]),
            ("state", "absent", ["sequence"]),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["acl_name"],
        module.params["extended"],
        module.params["rule"],
        module.params["sequence"],
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
