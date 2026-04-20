#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jerome Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: lldp_notification_enable
short_description: Enable or disable LLDP notifications on a D-Link DGS-1250 switch interface
description:
  - Configures the C(lldp notification enable) or C(lldp med notification enable) CLI command on a D-Link DGS-1250 switch.
  - Enables or disables LLDP or LLDP-MED notifications on an interface.
  - Corresponds to CLI command described in chapter 41-18 of the DGS-1250 CLI Reference Guide.
version_added: "0.14.0"
author:
  - "Jérôme Dumesnil (@jaydee-io)"
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/1)).
    type: str
    required: true
  med:
    description:
      - If true, configures LLDP-MED notifications instead of LLDP notifications.
    type: bool
    default: false
  state:
    description:
      - Whether to enable (C(enabled)) or disable (C(disabled)) notifications.
    type: str
    choices: [enabled, disabled]
    default: enabled
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable LLDP notifications on interface
  jaydee_io.dlink_dgs1250.lldp_notification_enable:
    interface: eth1/0/1

- name: Enable LLDP-MED notifications on interface
  jaydee_io.dlink_dgs1250.lldp_notification_enable:
    interface: eth1/0/1
    med: true

- name: Disable LLDP notifications on interface
  jaydee_io.dlink_dgs1250.lldp_notification_enable:
    interface: eth1/0/1
    state: disabled
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


def _build_commands(interface, med, state):
    prefix = "no " if state == "disabled" else ""
    if med:
        cmd = "%slldp med notification enable" % prefix
    else:
        cmd = "%slldp notification enable" % prefix
    return ["interface %s" % interface, cmd, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            med=dict(type="bool", default=False),
            state=dict(type="str", choices=[
                       "enabled", "disabled"], default="enabled"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interface"], module.params["med"], module.params["state"])
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
