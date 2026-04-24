#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: save_config
short_description: Save running-config to startup-config on a D-Link DGS-1250 switch
description:
  - Saves the current running configuration to the startup configuration on
    a D-Link DGS-1250 switch using the C(copy running-config startup-config) command.
  - Ensures that configuration changes persist across reboots.
version_added: "1.1.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
notes:
  - This command runs in Privileged EXEC Mode.
  - This module always reports C(changed=True) because there is no reliable way
    to detect whether the running-config differs from the startup-config.
"""

EXAMPLES = r"""
- name: Save running-config to startup-config
  jaydee_io.dlink_dgs1250.save_config:

- name: Save config after making changes
  jaydee_io.dlink_dgs1250.snmp_server_community:
    community: public
    access: ro
  notify: save config

# In handlers/main.yml:
# - name: save config
#   jaydee_io.dlink_dgs1250.save_config:
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


# ---------------------------------------------------------------------------
# Command builder
# ---------------------------------------------------------------------------

def _build_commands():
    """Build the CLI command list."""
    return ["copy running-config startup-config"]


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=True,
    )

    commands = _build_commands()

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
