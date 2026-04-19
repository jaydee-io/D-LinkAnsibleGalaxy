#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: aaa_ipv6_tacacs_source_interface
short_description: Configure IPv6 TACACS source interface on a D-Link DGS-1250 switch
description:
  - Configures the C(ipv6 tacacs source-interface) CLI command on a D-Link DGS-1250 switch.
  - Sets or removes the IPv6 source interface for TACACS+ packets.
  - Corresponds to CLI command described in chapter 8-16 of the DGS-1250 CLI Reference Guide.
version_added: "0.6.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Interface ID to use as source (e.g. C(vlan100)).
      - Required when C(state=present).
    type: str
  state:
    description:
      - C(present) to set the source interface, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set IPv6 TACACS source interface
  jaydee_io.dlink_dgs1250.aaa_ipv6_tacacs_source_interface:
    interface: vlan100

- name: Remove IPv6 TACACS source interface
  jaydee_io.dlink_dgs1250.aaa_ipv6_tacacs_source_interface:
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


# ---------------------------------------------------------------------------
# Command builder
# ---------------------------------------------------------------------------

def _build_commands(interface, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["no ipv6 tacacs source-interface"]
    return ["ipv6 tacacs source-interface %s" % interface]


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        required_if=[
            ("state", "present", ["interface"]),
        ],
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["interface"], module.params["state"])

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
