#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: aaa_radius_attribute_4
short_description: Configure RADIUS attribute 4 on a D-Link DGS-1250 switch
description:
  - Configures the C(radius-server attribute 4) CLI command on a D-Link DGS-1250 switch.
  - Sets or removes the NAS-IP-Address (attribute 4) for RADIUS packets.
  - Corresponds to CLI command described in chapter 8-20 of the DGS-1250 CLI Reference Guide.
version_added: "0.6.0"
author:
  - Jérôme Dumesnil
options:
  ip_address:
    description:
      - IP address to use as NAS-IP-Address.
    type: str
    required: true
  state:
    description:
      - C(present) to set the attribute, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Set RADIUS attribute 4
  jaydee_io.dlink_dgs1250.aaa_radius_attribute_4:
    ip_address: 10.0.0.1

- name: Remove RADIUS attribute 4
  jaydee_io.dlink_dgs1250.aaa_radius_attribute_4:
    ip_address: 10.0.0.1
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

def _build_commands(ip_address, state):
    """Build the CLI command list."""
    if state == "absent":
        return ["no radius-server attribute 4 %s" % ip_address]
    return ["radius-server attribute 4 %s" % ip_address]


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            ip_address=dict(type="str", required=True),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(module.params["ip_address"], module.params["state"])

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
