#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: aaa_authentication_mac_auth
short_description: Configure AAA authentication mac-auth on a D-Link DGS-1250 switch
description:
  - Configures the C(aaa authentication mac-auth default) CLI command on a D-Link DGS-1250 switch.
  - Sets the default method list for AAA MAC-based authentication.
  - Corresponds to CLI command described in chapter 8-5 of the DGS-1250 CLI Reference Guide.
version_added: "0.6.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  methods:
    description:
      - List of authentication methods (e.g. C(group radius)).
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
- name: Set AAA authentication mac-auth to use RADIUS
  jaydee_io.dlink_dgs1250.aaa_authentication_mac_auth:
    methods:
      - group radius

- name: Remove AAA authentication mac-auth configuration
  jaydee_io.dlink_dgs1250.aaa_authentication_mac_auth:
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

def _build_commands(methods, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["no aaa authentication mac-auth default"]
    return ["aaa authentication mac-auth default %s" % " ".join(methods)]


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            methods=dict(type="list", elements="str"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["methods"]),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(module.params["methods"], module.params["state"])

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
