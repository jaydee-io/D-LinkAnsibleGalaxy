#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dot1x_default
short_description: Reset 802.1X parameters to defaults on a D-Link DGS-1250 switch port
description:
  - Executes the C(dot1x default) CLI command on a D-Link DGS-1250 switch.
  - Resets all IEEE 802.1X parameters on the specified port to their default settings.
  - Corresponds to CLI command described in chapter 3-3 of the DGS-1250 CLI Reference Guide.
version_added: "0.2.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Physical port interface to reset (e.g. C(eth1/0/1)).
    required: true
    type: str
notes:
  - This command runs in Interface Configuration Mode.
  - Default values after reset are authentication disabled, control direction
    bidirectional, port control auto, forward PDU disabled, max request 2,
    server timer 30s, supplicant timer 30s, transmit interval 30s.
"""

EXAMPLES = r"""
- name: Reset 802.1X parameters on port 1
  jaydee_io.dlink_dgs1250.dot1x_default:
    interface: eth1/0/1
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

def _build_commands(interface):
    """Build the CLI command list for interface configuration."""
    return ["interface %s" % interface, "dot1x default"]


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str", required=True),
        ),
        supports_check_mode=True,
    )

    interface = module.params["interface"]
    commands = _build_commands(interface)

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
