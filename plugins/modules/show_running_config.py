#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: show_running_config
short_description: Display running configuration on a D-Link DGS-1250 switch
description:
  - Executes the C(show running-config) CLI command on a D-Link DGS-1250 switch.
  - Displays the commands in the running configuration file.
  - Corresponds to CLI command described in chapter 65-8 of the DGS-1250 CLI Reference Guide.
version_added: "0.18.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  mode:
    description:
      - Display mode. C(effective) shows only effective configuration, C(all) shows all including defaults.
    type: str
    choices: [effective, all]
  interface:
    description:
      - Display configuration for a specific interface.
    type: str
  vlan_id:
    description:
      - Display configuration for a specific VLAN.
    type: int
notes:
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Display running config
  jaydee_io.dlink_dgs1250.show_running_config:
  register: result

- name: Display effective running config
  jaydee_io.dlink_dgs1250.show_running_config:
    mode: effective
  register: result

- name: Display config for port 1
  jaydee_io.dlink_dgs1250.show_running_config:
    interface: eth1/0/1
  register: result
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
        run_command,
    )
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _build_command(mode, interface, vlan_id):
    cmd = "show running-config"
    if mode is not None:
        cmd += " %s" % mode
    if interface is not None:
        cmd += " interface %s" % interface
    if vlan_id is not None:
        cmd += " vlan %d" % vlan_id
    return cmd



def main():
    module = AnsibleModule(
        argument_spec=dict(
            mode=dict(type="str", choices=["effective", "all"]),
            interface=dict(type="str"),
            vlan_id=dict(type="int"),
        ),
        supports_check_mode=True,
    )
    command = _build_command(module.params["mode"], module.params["interface"], module.params["vlan_id"])
    if module.check_mode:
        module.exit_json(changed=False, commands=[command], raw_output="")
        return
    try:
        raw_output = run_command(module, command)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    module.exit_json(changed=False, raw_output=raw_output, commands=[command])


if __name__ == "__main__":
    main()
