#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: config_restore
short_description: Restore a configuration backup to a D-Link DGS-1250 switch
description:
  - Reads a configuration file from the Ansible controller and pushes each
    command to the D-Link DGS-1250 switch in Global Configuration Mode.
  - Typically used together with the M(jaydee_io.dlink_dgs1250.config_backup) module
    for disaster recovery or rollback.
  - Lines starting with C(!) and blank lines in the backup file are skipped.
version_added: "1.1.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  src:
    description:
      - Path on the Ansible controller to the configuration file to restore.
    type: path
    required: true
notes:
  - This command runs in Global Configuration Mode.
  - The configuration file should contain CLI commands as produced by
    C(show running-config).
  - After restoring, use M(jaydee_io.dlink_dgs1250.save_config) to persist
    changes to startup-config.
"""

EXAMPLES = r"""
- name: Restore a configuration backup
  jaydee_io.dlink_dgs1250.config_restore:
    src: /backups/sw1_backup.cfg

- name: Restore and save
  jaydee_io.dlink_dgs1250.config_restore:
    src: /backups/sw1_backup.cfg

- name: Persist restored configuration
  jaydee_io.dlink_dgs1250.save_config:
"""

RETURN = r"""
commands:
  description: List of CLI commands sent to the switch.
  returned: always
  type: list
  elements: str
raw_output:
  description: Raw text output from the switch CLI commands.
  returned: always
  type: str
"""

import os
from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import (
        run_commands, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


# ---------------------------------------------------------------------------
# Command builder
# ---------------------------------------------------------------------------

def _build_commands(config_text):
    """Parse a config file and return the list of CLI commands to send."""
    commands = []
    for line in config_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("!"):
            continue
        commands.append(stripped)
    return commands


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            src=dict(type="path", required=True),
        ),
        supports_check_mode=True,
    )

    src = module.params["src"]

    if not os.path.isfile(src):
        module.fail_json(msg="Source file not found: %s" % src)

    try:
        with open(src, "r") as f:
            config_text = f.read()
    except IOError as e:
        module.fail_json(msg="Failed to read %s: %s" % (src, str(e)))

    commands = _build_commands(config_text)

    if not commands:
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
