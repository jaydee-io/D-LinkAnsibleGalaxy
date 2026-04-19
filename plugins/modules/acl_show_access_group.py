#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: acl_show_access_group
short_description: Display access group information on a D-Link DGS-1250 switch
description:
  - Executes the C(show access-group) CLI command on a D-Link DGS-1250 switch.
  - Returns access list bindings per interface.
  - Corresponds to CLI command described in chapter 4-14 of the DGS-1250 CLI Reference Guide.
version_added: "0.3.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Physical port interface to query (e.g. C(eth1/0/1)).
      - If omitted, all interfaces with access lists are displayed.
    type: str
"""

EXAMPLES = r"""
- name: Show all access groups
  jaydee_io.dlink_dgs1250.acl_show_access_group:
  register: result

- name: Show access groups on port 1
  jaydee_io.dlink_dgs1250.acl_show_access_group:
    interface: eth1/0/1
  register: result
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
access_groups:
  description: List of access group bindings per interface.
  returned: success
  type: list
  elements: dict
  contains:
    interface:
      description: Interface name.
      type: str
    mac_acl:
      description: Inbound MAC access list name, or empty string if none.
      type: str
    ip_acl:
      description: Inbound IP access list name, or empty string if none.
      type: str
    ipv6_acl:
      description: Inbound IPv6 access list name, or empty string if none.
      type: str
"""

import re
from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import run_command
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


def _parse_access_groups(output):
    """
    Parse show access-group output.

    Expected format:
        eth1/0/1:
          Inbound mac access-list : simple-mac-acl(ID: 7998)
          Inbound ip access-list : simple-ip-acl(ID: 1998)
    """
    results = []
    current = None

    for line in output.splitlines():
        iface_match = re.match(r"^(eth\S+)\s*:", line)
        if iface_match:
            current = {
                "interface": iface_match.group(1),
                "mac_acl": "",
                "ip_acl": "",
                "ipv6_acl": "",
            }
            results.append(current)
            continue

        if current is None:
            continue

        acl_match = re.match(
            r"^\s+Inbound\s+(mac|ip|ipv6)\s+access-list\s*:\s*(.+)", line)
        if acl_match:
            acl_type = acl_match.group(1)
            acl_value = acl_match.group(2).strip()
            if acl_type == "mac":
                current["mac_acl"] = acl_value
            elif acl_type == "ip":
                current["ip_acl"] = acl_value
            elif acl_type == "ipv6":
                current["ipv6_acl"] = acl_value

    return results


def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str"),
        ),
        supports_check_mode=True,
    )

    command = "show access-group"
    if module.params["interface"]:
        command += " interface %s" % module.params["interface"]

    try:
        raw_output = run_command(module, command)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    result = dict(changed=False, raw_output=raw_output)
    result["access_groups"] = _parse_access_groups(raw_output)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
