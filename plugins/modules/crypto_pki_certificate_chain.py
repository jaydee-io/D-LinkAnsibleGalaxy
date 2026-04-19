#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: crypto_pki_certificate_chain
short_description: Enter Certificate Chain Configuration Mode on a D-Link DGS-1250 switch
description:
  - Executes the C(crypto pki certificate chain) CLI command on a D-Link DGS-1250 switch.
  - Enters the Certificate Chain Configuration Mode for a trust-point.
  - Corresponds to CLI command described in chapter 59-4 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  name:
    description:
      - The trust-point name.
    type: str
    required: true
notes:
  - This command runs in Global Configuration Mode.
  - This module is primarily used as a building block. Consider using C(ssl_no_certificate) for direct operations.
"""

EXAMPLES = r"""
- name: Enter certificate chain mode
  jaydee_io.dlink_dgs1250.crypto_pki_certificate_chain:
    name: TP1
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
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, MODE_GLOBAL_CONFIG


def _build_commands(name):
    return ["crypto pki certificate chain %s" % name, "exit"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type="str", required=True),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(module.params["name"])
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
