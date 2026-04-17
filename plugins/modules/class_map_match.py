#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: class_map_match
short_description: Configure match criteria inside a class-map on a D-Link DGS-1250 switch
description:
  - Configures the C(match) CLI command inside a class-map on a D-Link DGS-1250 switch.
  - Defines the match criteria for a class-map.
  - Corresponds to CLI command described in chapter 54-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil
options:
  class_map:
    description:
      - Name of the class map to modify.
    type: str
    required: true
  criteria:
    description:
      - Match criteria type.
    type: str
    required: true
    choices: [access-group-name, cos, dscp, ip-dscp, precedence, ip-precedence, protocol, vlan]
  value:
    description:
      - Value associated with the criteria (ACL name, CoS list, DSCP list, precedence list, protocol name, or VLAN list).
    type: str
    required: true
  state:
    description:
      - C(present) to add the match, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Class-map Configuration Mode.
"""

EXAMPLES = r"""
- name: Match access-list
  jaydee_io.dlink_dgs1250.class_map_match:
    class_map: class-home-user
    criteria: access-group-name
    value: acl-home-user

- name: Match CoS 1,2,3
  jaydee_io.dlink_dgs1250.class_map_match:
    class_map: cos
    criteria: cos
    value: "1,2,3"

- name: Match protocol ipv6
  jaydee_io.dlink_dgs1250.class_map_match:
    class_map: class_home_user
    criteria: protocol
    value: ipv6
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


CRITERIA_MAP = {
    "access-group-name": "access-group name",
    "cos": "cos",
    "dscp": "dscp",
    "ip-dscp": "ip dscp",
    "precedence": "precedence",
    "ip-precedence": "ip precedence",
    "protocol": "protocol",
    "vlan": "vlan",
}


def _build_commands(class_map, criteria, value, state):
    cli_kw = CRITERIA_MAP[criteria]
    match_cmd = "match %s %s" % (cli_kw, value)
    commands = ["class-map %s" % class_map]
    if state == "absent":
        commands.append("no " + match_cmd)
    else:
        commands.append(match_cmd)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            class_map=dict(type="str", required=True),
            criteria=dict(type="str", required=True,
                          choices=list(CRITERIA_MAP.keys())),
            value=dict(type="str", required=True),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["class_map"],
        module.params["criteria"],
        module.params["value"],
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
