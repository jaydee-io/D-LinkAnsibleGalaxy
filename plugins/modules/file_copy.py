#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: file_copy
short_description: Copy files on a D-Link DGS-1250 switch
description:
  - Executes the C(copy) CLI command on a D-Link DGS-1250 switch.
  - Copies a file to another file, uploads/downloads via TFTP, saves configuration.
  - Corresponds to CLI command described in chapter 65-6 of the DGS-1250 CLI Reference Guide.
version_added: "0.18.0"
author:
  - Jérôme Dumesnil
options:
  source:
    description:
      - The source URL or keyword (running-config, startup-config, log, attack-log, flash:, tftp:).
    type: str
    required: true
  destination:
    description:
      - The destination URL or keyword (running-config, startup-config, flash:, tftp:).
    type: str
    required: true
notes:
  - This module requires C(ansible_network_os=jaydee_io.dlink_dgs1250.dgs1250) and
    C(ansible_connection=ansible.netcommon.network_cli) set in the inventory.
  - This command runs in Privileged EXEC Mode.
"""

EXAMPLES = r"""
- name: Save running config to startup config
  jaydee_io.dlink_dgs1250.copy:
    source: running-config
    destination: startup-config

- name: Download config from TFTP
  jaydee_io.dlink_dgs1250.copy:
    source: "tftp: //10.1.1.254/switch-config.cfg"
    destination: running-config
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
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_PRIVILEGED


def _build_commands(source, destination):
    return ["copy %s %s" % (source, destination)]




def main():
    module = AnsibleModule(
        argument_spec=dict(
            source=dict(type="str", required=True),
            destination=dict(type="str", required=True),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["source"], module.params["destination"])
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
