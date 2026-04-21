#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: aaa_accounting_network
short_description: Configure AAA accounting network on a D-Link DGS-1250 switch
description:
  - Configures the C(aaa accounting network default) CLI command on a D-Link DGS-1250 switch.
  - Sets the default method list for AAA network accounting.
  - Corresponds to CLI command described in chapter 8-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.6.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  methods:
    description:
      - List of accounting methods (e.g. C(group radius), C(none)).
      - Required when C(state=present).
    type: list
    elements: str
  state:
    description:
      - C(present) to configure the accounting method list, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set AAA accounting network to use RADIUS
  jaydee_io.dlink_dgs1250.aaa_accounting_network:
    methods:
      - group radius

- name: Disable AAA accounting network
  jaydee_io.dlink_dgs1250.aaa_accounting_network:
    methods:
      - none

- name: Remove AAA accounting network configuration
  jaydee_io.dlink_dgs1250.aaa_accounting_network:
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


# ---------------------------------------------------------------------------
# Command builder
# ---------------------------------------------------------------------------

def _build_commands(methods, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["no aaa accounting network default"]
    if methods == ["none"]:
        return ["aaa accounting network default none"]
    return ["aaa accounting network default start-stop %s" % " ".join(methods)]


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            methods=dict(type="list", elements="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["methods"]),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["methods"], module.params["state"])

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
