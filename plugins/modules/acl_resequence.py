#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: acl_resequence
short_description: Re-sequence ACL entries on a D-Link DGS-1250 switch
description:
  - Configures the C(access-list resequence) CLI command on a D-Link DGS-1250 switch.
  - Re-sequences the starting sequence number and increment of an access list.
  - Use C(state=absent) to revert to default sequencing.
  - Corresponds to CLI command described in chapter 4-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.3.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  name:
    description:
      - Name or number of the access list to re-sequence.
    type: str
    required: true
  starting_sequence:
    description:
      - Starting sequence number (1-65535). Required when C(state=present).
    type: int
  increment:
    description:
      - Increment between sequence numbers (1-32). Required when C(state=present).
    type: int
  state:
    description:
      - C(present) to re-sequence, C(absent) to revert to default.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command requires Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Re-sequence ACL 'R&D' starting at 1 with increment 2
  jaydee_io.dlink_dgs1250.acl_resequence:
    name: R&D
    starting_sequence: 1
    increment: 2

- name: Revert ACL 'R&D' to default sequencing
  jaydee_io.dlink_dgs1250.acl_resequence:
    name: R&D
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


# ---------------------------------------------------------------------------
# Command builder
# ---------------------------------------------------------------------------

def _build_commands(name, starting_sequence, increment, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["no access-list resequence"]
    return ["access-list resequence %s %d %d" % (name, starting_sequence, increment)]


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type="str", required=True),
            starting_sequence=dict(type="int"),
            increment=dict(type="int"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["starting_sequence", "increment"]),
        ],
        supports_check_mode=True,
    )

    name = module.params["name"]
    starting_sequence = module.params["starting_sequence"]
    increment = module.params["increment"]
    state = module.params["state"]

    commands = _build_commands(name, starting_sequence, increment, state)

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
