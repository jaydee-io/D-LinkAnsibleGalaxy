#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dhcp_relay_option_hex
short_description: Configure DHCP option matching pattern for a DHCP class on a D-Link DGS-1250 switch
description:
  - Configures the C(option hex) CLI command in DHCP Class Configuration Mode on a D-Link DGS-1250 switch.
  - Corresponds to CLI command described in chapter 16-17 of the DGS-1250 CLI Reference Guide.
version_added: "0.9.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  dhcp_class:
    description:
      - The DHCP class name to configure.
    type: str
    required: true
  code:
    description:
      - The DHCP option number.
    type: int
    required: true
  pattern:
    description:
      - The hex pattern of the specified DHCP option.
    type: str
    required: true
  wildcard:
    description:
      - If C(true), do not match the remaining bits of the option.
    type: bool
    default: false
  bitmask:
    description:
      - The hex bit mask for masking of the pattern.
    type: str
  state:
    description:
      - C(present) to add the option, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in DHCP Class Configuration Mode.
"""

EXAMPLES = r"""
- name: Add option 60 hex pattern to class Service-A
  jaydee_io.dlink_dgs1250.dhcp_relay_option_hex:
    dhcp_class: Service-A
    code: 60
    pattern: "112233"

- name: Remove option 60 hex pattern from class Service-A
  jaydee_io.dlink_dgs1250.dhcp_relay_option_hex:
    dhcp_class: Service-A
    code: 60
    pattern: "112233"
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


def _build_commands(dhcp_class, code, pattern, wildcard, bitmask, state):
    """Build the CLI command list."""
    commands = ["ip dhcp class %s" % dhcp_class]
    base = "option %s hex %s" % (code, pattern)
    if state == "absent":
        cmd = "no %s" % base
    else:
        cmd = base
        if wildcard:
            cmd += " *"
        if bitmask:
            cmd += " bitmask %s" % bitmask
    commands.append(cmd)
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            dhcp_class=dict(type="str", required=True),
            code=dict(type="int", required=True),
            pattern=dict(type="str", required=True),
            wildcard=dict(type="bool", default=False),
            bitmask=dict(type="str"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["dhcp_class"],
        module.params["code"],
        module.params["pattern"],
        module.params["wildcard"],
        module.params["bitmask"],
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
