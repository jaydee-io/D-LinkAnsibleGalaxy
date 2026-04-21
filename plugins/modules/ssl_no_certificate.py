#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: ssl_no_certificate
short_description: Delete an imported certificate from a trust point on a D-Link DGS-1250 switch
description:
  - Executes the C(no certificate) CLI command in Certificate Chain Configuration Mode on a D-Link DGS-1250 switch.
  - Deletes an imported certificate from a trust point.
  - Corresponds to CLI command described in chapter 59-1 of the DGS-1250 CLI Reference Guide.
version_added: "0.17.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  trustpoint:
    description:
      - The trust-point name containing the certificate.
    type: str
    required: true
  certificate:
    description:
      - The name of the certificate to delete.
    type: str
    required: true
notes:
  - This command runs in Certificate Chain Configuration Mode.
"""

EXAMPLES = r"""
- name: Delete certificate from trust point
  jaydee_io.dlink_dgs1250.ssl_no_certificate:
    trustpoint: gaa
    certificate: tongken.ca
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
        run_commands, is_config_present, build_config_diff, MODE_GLOBAL_CONFIG,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, is_config_present, build_config_diff, MODE_GLOBAL_CONFIG


def _build_commands(trustpoint, certificate):
    return [
        "crypto pki certificate chain %s" % trustpoint,
        "no certificate %s" % certificate,
        "exit",
    ]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            trustpoint=dict(type="str", required=True),
            certificate=dict(type="str", required=True),
        ),
        supports_check_mode=True,
    )
    commands = _build_commands(
        module.params["trustpoint"], module.params["certificate"])
    if is_config_present(module, commands):
        module.exit_json(changed=False, commands=[], raw_output="")
        return
    diff = build_config_diff(module, commands) if module._diff else None
    if module.check_mode:
        result = dict(changed=True, commands=commands, raw_output="")
        if diff:
            result['diff'] = diff
        module.exit_json(**result)
        return
    try:
        raw_output = run_commands(module, commands, mode=MODE_GLOBAL_CONFIG)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))
    result = dict(changed=True, raw_output=raw_output, commands=commands)
    if diff:
        result['diff'] = diff
    module.exit_json(**result)


if __name__ == "__main__":
    main()
