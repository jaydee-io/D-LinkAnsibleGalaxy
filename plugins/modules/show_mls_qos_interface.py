#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: show_mls_qos_interface
short_description: Display port-level QoS configuration on a D-Link DGS-1250 switch
description:
  - Displays the output of the C(show mls qos interface) CLI command.
  - Corresponds to CLI command described in chapter 54-17 of the DGS-1250 CLI Reference Guide.
version_added: "0.16.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Interface or interface range to display (e.g. C(eth1/0/2-5)).
    type: str
    required: true
  info:
    description:
      - Which configuration item to display.
    type: str
    required: true
    choices: [cos, scheduler, trust, rate-limit, queue-rate-limit, dscp-mutation, map-dscp-cos]
notes:
  - This command runs in User/Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Show CoS for eth1/0/2-5
  jaydee_io.dlink_dgs1250.show_mls_qos_interface:
    interface: eth1/0/2-5
    info: cos

- name: Show DSCP to CoS map
  jaydee_io.dlink_dgs1250.show_mls_qos_interface:
    interface: eth1/0/1
    info: map-dscp-cos
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
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


INFO_MAP = {
    "cos": "cos",
    "scheduler": "scheduler",
    "trust": "trust",
    "rate-limit": "rate-limit",
    "queue-rate-limit": "queue-rate-limit",
    "dscp-mutation": "dscp-mutation",
    "map-dscp-cos": "map dscp-cos",
}


def _build_command(interface, info):
    return "show mls qos interface %s %s" % (interface, INFO_MAP[info])


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
            info=dict(type="str", required=True,
                      choices=list(INFO_MAP.keys())),
        ),
        supports_check_mode=True,
    )
    command = _build_command(module.params["interface"], module.params["info"])
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
