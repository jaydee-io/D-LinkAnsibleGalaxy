#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: aaa_authentication_login
short_description: Configure AAA authentication login on a D-Link DGS-1250 switch
description:
  - Configures the C(aaa authentication login) CLI command on a D-Link DGS-1250 switch.
  - Sets a named or default method list for AAA login authentication.
  - Corresponds to CLI command described in chapter 8-4 of the DGS-1250 CLI Reference Guide.
version_added: "0.6.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  list_name:
    description:
      - Name of the method list, or C(default) for the default list.
    type: str
    default: default
  methods:
    description:
      - List of authentication methods (e.g. C(group group2), C(local)).
      - Required when C(state=present).
    type: list
    elements: str
  state:
    description:
      - C(present) to configure the method list, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set default AAA login authentication
  jaydee_io.dlink_dgs1250.aaa_authentication_login:
    methods:
      - group group2
      - local

- name: Set named AAA login authentication list
  jaydee_io.dlink_dgs1250.aaa_authentication_login:
    list_name: MY_LIST
    methods:
      - group radius

- name: Remove AAA login authentication list
  jaydee_io.dlink_dgs1250.aaa_authentication_login:
    list_name: MY_LIST
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


# ---------------------------------------------------------------------------
# Command builder
# ---------------------------------------------------------------------------

def _build_commands(list_name, methods, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["no aaa authentication login %s" % list_name]
    return ["aaa authentication login %s %s" % (list_name, " ".join(methods))]


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            list_name=dict(type="str", default="default"),
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
        module.params["list_name"],
        module.params["methods"],
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
