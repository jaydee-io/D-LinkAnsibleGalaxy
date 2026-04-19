#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: mgmt_ip_http_secure_server
short_description: Enable or disable the HTTPS server on a D-Link DGS-1250 switch
description:
  - Configures the C(ip http secure-server) CLI command on a D-Link DGS-1250 switch.
  - Optionally specifies an SSL service policy.
  - Corresponds to CLI command described in chapter 5-5 of the DGS-1250 CLI Reference Guide.
version_added: "0.4.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  state:
    description:
      - C(enabled) to enable the HTTPS server, C(disabled) to disable it.
    type: str
    choices: [enabled, disabled]
    default: enabled
  ssl_service_policy:
    description:
      - Name of the SSL service policy to use for HTTPS.
      - Only used when C(state=enabled).
    type: str
"""

EXAMPLES = r"""
- name: Enable HTTPS server with SSL policy 'sp1'
  jaydee_io.dlink_dgs1250.mgmt_ip_http_secure_server:
    ssl_service_policy: sp1

- name: Enable HTTPS server with built-in certificate
  jaydee_io.dlink_dgs1250.mgmt_ip_http_secure_server:

- name: Disable HTTPS server
  jaydee_io.dlink_dgs1250.mgmt_ip_http_secure_server:
    state: disabled
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


def _build_commands(state, ssl_service_policy):
    if state == "disabled":
        return ["no ip http secure-server"]
    cmd = "ip http secure-server"
    if ssl_service_policy:
        cmd += " ssl-service-policy %s" % ssl_service_policy
    return [cmd]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type="str", choices=["enabled", "disabled"], default="enabled"),
            ssl_service_policy=dict(type="str"),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(module.params["state"], module.params["ssl_service_policy"])

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
