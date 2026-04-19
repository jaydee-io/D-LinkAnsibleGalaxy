#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dai_clear_arp_inspection_statistics
short_description: Clear Dynamic ARP Inspection statistics on a D-Link DGS-1250 switch
description:
  - Executes the C(clear ip arp inspection statistics) CLI command on a D-Link DGS-1250 switch.
  - Clears the dynamic ARP inspection statistics for all VLANs or a specific VLAN.
  - Corresponds to CLI command described in chapter 25-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.10.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  vlan_id:
    description:
      - The VLAN ID to clear statistics for (e.g. C(1) or C(1-10)).
      - If not specified, statistics for all VLANs are cleared.
    type: str
notes:
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Clear DAI statistics for all VLANs
  jaydee_io.dlink_dgs1250.dai_clear_arp_inspection_statistics:

- name: Clear DAI statistics for VLAN 1
  jaydee_io.dlink_dgs1250.dai_clear_arp_inspection_statistics:
    vlan_id: "1"
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
        run_commands, MODE_PRIVILEGED,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_PRIVILEGED


def _build_commands(vlan_id):
    """Build the CLI command list."""
    if vlan_id:
        return ["clear ip arp inspection statistics vlan %s" % vlan_id]
    else:
        return ["clear ip arp inspection statistics all"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            vlan_id=dict(type="str"),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["vlan_id"])
    if module.check_mode:
        module.exit_json(changed=True, commands=commands, raw_output="")
        return
    try:
        raw_output = run_commands(module, commands, mode=MODE_PRIVILEGED)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    module.exit_json(changed=True, raw_output=raw_output, commands=commands)


if __name__ == "__main__":
    main()
