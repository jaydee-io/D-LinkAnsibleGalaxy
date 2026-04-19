#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: crypto_pki_certificate_generate
short_description: Generate a self-signed certificate on a D-Link DGS-1250 switch
description:
  - Executes the C(crypto pki certificate generate) CLI command on a D-Link DGS-1250 switch.
  - Generates a new self-signed RSA certificate with 2048-bit key length.
  - Corresponds to CLI command described in chapter 59-9 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options: {}
notes:
  - This command runs in Global Configuration Mode.
"""

EXAMPLES = r"""
- name: Generate self-signed certificate
  jaydee_io.dlink_dgs1250.crypto_pki_certificate_generate:
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


def _build_commands():
    return ["crypto pki certificate generate"]



def main():
    module = AnsibleModule(
        argument_spec=dict(

        ),
        supports_check_mode=True,
    )
    commands = _build_commands()
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
