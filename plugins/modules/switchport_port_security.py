#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: switchport_port_security
short_description: Configure port security on an interface on a D-Link DGS-1250 switch
description:
  - Configures the C(switchport port-security) CLI command on a D-Link DGS-1250 switch.
  - Configures port security settings including maximum addresses, violation action, and security mode.
  - Corresponds to CLI command described in chapter 50-4 of the DGS-1250 CLI Reference Guide.
version_added: "0.15.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/1)).
    type: str
    required: true
  maximum:
    description:
      - The maximum number of secure MAC addresses (0 to 64, default 32).
    type: int
  violation:
    description:
      - The violation action.
    type: str
    choices: [protect, restrict, shutdown]
  mode:
    description:
      - The security mode.
    type: str
    choices: [permanent, delete-on-timeout]
  mac_address:
    description:
      - A secure MAC address to add or remove.
    type: str
  permanent:
    description:
      - Whether the MAC address entry is permanent.
    type: bool
  vlan_id:
    description:
      - VLAN ID for the MAC address entry.
    type: int
  state:
    description:
      - C(present) to configure port security, C(absent) to disable or remove settings.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Enable port security with maximum 10 addresses
  jaydee_io.dlink_dgs1250.switchport_port_security:
    interface: eth1/0/1
    maximum: 10

- name: Set violation action to shutdown
  jaydee_io.dlink_dgs1250.switchport_port_security:
    interface: eth1/0/1
    violation: shutdown

- name: Set security mode to permanent
  jaydee_io.dlink_dgs1250.switchport_port_security:
    interface: eth1/0/1
    mode: permanent

- name: Add a secure MAC address
  jaydee_io.dlink_dgs1250.switchport_port_security:
    interface: eth1/0/1
    mac_address: "0080.0070.0007"

- name: Disable port security
  jaydee_io.dlink_dgs1250.switchport_port_security:
    interface: eth1/0/1
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


def _build_commands(interface, maximum, violation, mode, mac_address, permanent, vlan_id, state):
    """Build the CLI command list."""
    commands = ["interface %s" % interface]
    if state == "absent":
        if mac_address:
            cmd = "no switchport port-security mac-address %s" % mac_address
            if vlan_id is not None:
                cmd += " vlan %d" % vlan_id
            commands.append(cmd)
        elif maximum is not None:
            commands.append("no switchport port-security maximum")
        elif violation is not None:
            commands.append("no switchport port-security violation")
        elif mode is not None:
            commands.append("no switchport port-security mode")
        else:
            commands.append("no switchport port-security")
    else:
        if maximum is not None:
            commands.append("switchport port-security maximum %d" % maximum)
        if violation is not None:
            commands.append(
                "switchport port-security violation %s" % violation)
        if mode is not None:
            commands.append("switchport port-security mode %s" % mode)
        if mac_address:
            cmd = "switchport port-security mac-address"
            if permanent:
                cmd += " permanent"
            cmd += " %s" % mac_address
            if vlan_id is not None:
                cmd += " vlan %d" % vlan_id
            commands.append(cmd)
        if maximum is None and violation is None and mode is None and mac_address is None:
            commands.append("switchport port-security")
    commands.append("exit")
    return commands


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            maximum=dict(type="int"),
            violation=dict(type="str", choices=[
                           "protect", "restrict", "shutdown"]),
            mode=dict(type="str", choices=["permanent", "delete-on-timeout"]),
            mac_address=dict(type="str"),
            permanent=dict(type="bool"),
            vlan_id=dict(type="int"),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["interface"],
        module.params["maximum"],
        module.params["violation"],
        module.params["mode"],
        module.params["mac_address"],
        module.params["permanent"],
        module.params["vlan_id"],
        module.params["state"],
    )
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
