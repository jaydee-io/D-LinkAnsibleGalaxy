#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jerome Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: lldp_subtype
short_description: Configure LLDP port ID subtype on a D-Link DGS-1250 switch interface
description:
  - Configures the C(lldp subtype port-id) CLI command on a D-Link DGS-1250 switch.
  - Configures how the port ID is encoded in LLDP TLVs.
  - Corresponds to CLI command described in chapter 41-19 of the DGS-1250 CLI Reference Guide.
version_added: "0.14.0"
author:
  - Jerome Dumesnil
options:
  interface:
    description:
      - The interface to configure (e.g. C(eth1/0/1)).
    type: str
    required: true
  subtype:
    description:
      - C(mac-address) encodes port ID as MAC Address.
      - C(local) encodes port ID as locally assigned port number.
    type: str
    required: true
    choices: [mac-address, local]
notes:
  - This command runs in Interface Configuration Mode.
"""

EXAMPLES = r"""
- name: Set port ID subtype to MAC address
  jaydee_io.dlink_dgs1250.lldp_subtype:
    interface: eth1/0/1
    subtype: mac-address

- name: Set port ID subtype to local
  jaydee_io.dlink_dgs1250.lldp_subtype:
    interface: eth1/0/1
    subtype: local
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


def _build_commands(interface, subtype):
    return ["interface %s" % interface, "lldp subtype port-id %s" % subtype, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            subtype=dict(type="str", required=True, choices=["mac-address", "local"]),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["interface"], module.params["subtype"])
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
