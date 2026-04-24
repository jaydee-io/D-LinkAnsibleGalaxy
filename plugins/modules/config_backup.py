#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: config_backup
short_description: Backup the running configuration of a D-Link DGS-1250 switch
description:
  - Retrieves the full running configuration from a D-Link DGS-1250 switch
    using the C(show running-config) command and saves it to a local file.
  - Useful for disaster recovery, auditing, and rollback scenarios.
version_added: "1.1.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  dest:
    description:
      - Absolute or relative path on the Ansible controller where the backup
        file will be written.
    type: path
    required: true
notes:
  - This command runs in Privileged EXEC Mode.
  - The file is written on the Ansible controller, not on the switch.
"""

EXAMPLES = r"""
- name: Backup running-config to a local file
  jaydee_io.dlink_dgs1250.config_backup:
    dest: /tmp/sw1_backup.cfg

- name: Backup with hostname and date in filename
  jaydee_io.dlink_dgs1250.config_backup:
    dest: "/backups/{{ inventory_hostname }}_{{ ansible_date_time.date }}.cfg"
"""

RETURN = r"""
dest:
  description: Path of the backup file on the Ansible controller.
  returned: always
  type: str
commands:
  description: List of CLI commands sent to the switch.
  returned: always
  type: list
  elements: str
"""

import os
from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import (
        get_running_config,
    )
except ImportError:
    import sys
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import get_running_config


# ---------------------------------------------------------------------------
# Command builder
# ---------------------------------------------------------------------------

def _build_command():
    """Return the CLI command used for backup."""
    return "show running-config"


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            dest=dict(type="path", required=True),
        ),
        supports_check_mode=True,
    )

    dest = module.params["dest"]
    commands = [_build_command()]

    if module.check_mode:
        module.exit_json(changed=True, commands=commands, dest=dest)
        return

    try:
        config = get_running_config(module)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    try:
        dest_dir = os.path.dirname(dest)
        if dest_dir and not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        with open(dest, "w") as f:
            f.write(config)
    except IOError as e:
        module.fail_json(msg="Failed to write backup to %s: %s" % (dest, str(e)))

    module.exit_json(changed=True, commands=commands, dest=dest)


if __name__ == "__main__":
    main()
