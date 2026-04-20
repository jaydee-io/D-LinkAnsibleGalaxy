#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dot1x_timeout
short_description: Configure 802.1X timers on a D-Link DGS-1250 switch port
description:
  - Configures the C(dot1x timeout) CLI command on a D-Link DGS-1250 switch.
  - Sets the server-timeout, supplicant-timeout, and/or tx-period timers.
  - Use C(state=absent) to revert specified timers to their default values (30 seconds each).
  - Corresponds to CLI command described in chapter 3-11 of the DGS-1250 CLI Reference Guide.
version_added: "0.2.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Physical port interface to configure (e.g. C(eth1/0/1)).
    required: true
    type: str
  server_timeout:
    description:
      - Seconds the switch waits for the authentication server before timing out.
      - Range is 1 to 65535. Default is 30.
    type: int
  supp_timeout:
    description:
      - Seconds the switch waits for the supplicant response before timing out.
      - Range is 1 to 65535. Default is 30.
    type: int
  tx_period:
    description:
      - Seconds the switch waits before retransmitting an EAP-Request/Identity frame.
      - Range is 1 to 65535. Default is 30.
    type: int
  state:
    description:
      - Whether to set (C(present)) or reset to defaults (C(absent)) the specified timers.
      - When C(absent), specify which timers to reset via C(server_timeout), C(supp_timeout), C(tx_period)
        set to any value, or omit all to reset all three.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Set all three timers on port 1
  jaydee_io.dlink_dgs1250.dot1x_timeout:
    interface: eth1/0/1
    server_timeout: 15
    supp_timeout: 15
    tx_period: 10

- name: Set only tx-period on port 1
  jaydee_io.dlink_dgs1250.dot1x_timeout:
    interface: eth1/0/1
    tx_period: 10

- name: Reset all timers to defaults on port 1
  jaydee_io.dlink_dgs1250.dot1x_timeout:
    interface: eth1/0/1
    state: absent

- name: Reset only tx-period to default on port 1
  jaydee_io.dlink_dgs1250.dot1x_timeout:
    interface: eth1/0/1
    tx_period: 0
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

def _build_commands(interface, state, server_timeout, supp_timeout, tx_period):
    """Build the CLI command list for interface configuration."""
    commands = ["interface %s" % interface]

    if state == "absent":
        has_specific = server_timeout is not None or supp_timeout is not None or tx_period is not None
        if not has_specific or server_timeout is not None:
            commands.append("no dot1x timeout server-timeout")
        if not has_specific or supp_timeout is not None:
            commands.append("no dot1x timeout supp-timeout")
        if not has_specific or tx_period is not None:
            commands.append("no dot1x timeout tx-period")
    else:
        if server_timeout is not None:
            commands.append("dot1x timeout server-timeout %d" % server_timeout)
        if supp_timeout is not None:
            commands.append("dot1x timeout supp-timeout %d" % supp_timeout)
        if tx_period is not None:
            commands.append("dot1x timeout tx-period %d" % tx_period)

    return commands


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            server_timeout=dict(type="int"),
            supp_timeout=dict(type="int"),
            tx_period=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )

    interface = module.params["interface"]
    state = module.params["state"]
    server_timeout = module.params["server_timeout"]
    supp_timeout = module.params["supp_timeout"]
    tx_period = module.params["tx_period"]

    if state == "present" and server_timeout is None and supp_timeout is None and tx_period is None:
        module.fail_json(
            msg="At least one of 'server_timeout', 'supp_timeout', or 'tx_period' must be specified when state is 'present'.")

    for name, value in [("server_timeout", server_timeout), ("supp_timeout", supp_timeout), ("tx_period", tx_period)]:
        if state == "present" and value is not None and (value < 1 or value > 65535):
            module.fail_json(msg="'%s' must be between 1 and 65535." % name)

    commands = _build_commands(
        interface, state, server_timeout, supp_timeout, tx_period)

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
