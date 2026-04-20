#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: mgmt_ip_http_access_class
short_description: Restrict HTTP/HTTPS access with an IP ACL on a D-Link DGS-1250 switch
description:
  - Configures the C(ip http access-class) or C(ip https access-class) CLI command.
  - Applies or removes a standard IP access list to restrict access to the HTTP or HTTPS server.
  - Corresponds to CLI command described in chapter 5-6 of the DGS-1250 CLI Reference Guide.
version_added: "0.4.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  protocol:
    description:
      - Protocol to restrict.
    type: str
    required: true
    choices: [http, https]
  acl_name:
    description:
      - Name of the standard IP access list.
    type: str
    required: true
  state:
    description:
      - C(present) to apply the access class, C(absent) to remove it.
    type: str
    choices: [present, absent]
    default: present
"""

EXAMPLES = r"""
- name: Restrict HTTP access with ACL 'http-filter'
  jaydee_io.dlink_dgs1250.mgmt_ip_http_access_class:
    protocol: http
    acl_name: http-filter

- name: Remove HTTPS access restriction
  jaydee_io.dlink_dgs1250.mgmt_ip_http_access_class:
    protocol: https
    acl_name: http-filter
    state: absent
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


def _build_commands(protocol, acl_name, state):
    prefix = "" if state == "present" else "no "
    return ["%sip %s access-class %s" % (prefix, protocol, acl_name)]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            protocol=dict(type="str", required=True,
                          choices=["http", "https"]),
            acl_name=dict(type="str", required=True),
            state=dict(type="str", choices=[
                       "present", "absent"], default="present"),
        ),
        supports_check_mode=True,
    )

    commands = _build_commands(
        module.params["protocol"], module.params["acl_name"], module.params["state"])

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
