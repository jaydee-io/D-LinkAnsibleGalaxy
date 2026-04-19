#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: ip_source_binding
short_description: Configure IP source guard static binding on a D-Link DGS-1250 switch
description:
  - Configures the C(ip source binding) CLI command on a D-Link DGS-1250 switch.
  - Creates or deletes a static entry used for IP source guard checking.
  - Corresponds to CLI command described in chapter 35-2 of the DGS-1250 CLI Reference Guide.
version_added: "0.12.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  mac_addr:
    description:
      - The MAC address of the binding entry (e.g. C(00-01-02-03-04-05)).
    type: str
    required: true
  vlan_id:
    description:
      - The VLAN ID that the valid host belongs to.
    type: int
    required: true
  ip_addr:
    description:
      - The IP address of the binding entry (e.g. C(10.1.1.1)).
    type: str
    required: true
  interface_id:
    description:
      - The interface that the valid host is connected to (e.g. C(eth1/0/10)).
    type: str
    required: true
  state:
    description:
      - C(present) to create, C(absent) to delete the static binding entry.
    type: str
    choices: [present, absent]
    default: present
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Create an IP source guard static binding
  jaydee_io.dlink_dgs1250.ip_source_binding:
    mac_addr: "00-01-02-03-04-05"
    vlan_id: 2
    ip_addr: "10.1.1.1"
    interface_id: eth1/0/10

- name: Delete an IP source guard static binding
  jaydee_io.dlink_dgs1250.ip_source_binding:
    mac_addr: "00-01-02-03-04-05"
    vlan_id: 2
    ip_addr: "10.1.1.1"
    interface_id: eth1/0/10
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


def _build_commands(mac_addr, vlan_id, ip_addr, interface_id, state):
    prefix = "no " if state == "absent" else ""
    return [
        "%sip source binding %s vlan %d %s interface %s"
        % (prefix, mac_addr, vlan_id, ip_addr, interface_id)
    ]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            mac_addr=dict(type="str", required=True),
            vlan_id=dict(type="int", required=True),
            ip_addr=dict(type="str", required=True),
            interface_id=dict(type="str", required=True),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["mac_addr"],
        module.params["vlan_id"],
        module.params["ip_addr"],
        module.params["interface_id"],
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
