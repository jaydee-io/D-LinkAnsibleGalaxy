#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v2.0+ (see COPYING or https://www.gnu.org/licenses/gpl-2.0.txt)

DOCUMENTATION = r"""
---
module: aaa_show_radius_statistics
short_description: Display RADIUS statistics on a D-Link DGS-1250 switch
description:
  - Executes the C(show radius statistics) CLI command on a D-Link DGS-1250 switch.
  - Returns parsed RADIUS server statistics for all configured servers.
  - Corresponds to CLI command described in chapter 8-28 of the DGS-1250 CLI Reference Guide.
version_added: "0.6.0"
author:
  - Jérôme Dumesnil
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options: {}
notes:
"""

EXAMPLES = r"""
- name: Show RADIUS statistics
  jaydee_io.dlink_dgs1250.aaa_show_radius_statistics:
  register: radius_stats
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
servers:
  description: List of RADIUS server statistics.
  returned: always
  type: list
  elements: dict
  contains:
    server:
      description: Server IP address.
      type: str
    auth_port:
      description: Authentication port.
      type: int
    state:
      description: Server state (Up or Down).
      type: str
    round_trip_time:
      description: Round trip time in seconds.
      type: int
    access_requests:
      description: Number of Access-Request packets sent.
      type: int
    access_accepts:
      description: Number of Access-Accept packets received.
      type: int
    access_rejects:
      description: Number of Access-Reject packets received.
      type: int
    access_challenges:
      description: Number of Access-Challenge packets received.
      type: int
    retransmissions:
      description: Number of retransmissions.
      type: int
    malformed_responses:
      description: Number of malformed responses.
      type: int
    bad_authenticators:
      description: Number of bad authenticators.
      type: int
    pending_requests:
      description: Number of pending requests.
      type: int
    timeouts:
      description: Number of timeouts.
      type: int
    unknown_types:
      description: Number of unknown type packets.
      type: int
    packets_dropped:
      description: Number of dropped packets.
      type: int
"""

import re
from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import run_command
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_command


# ---------------------------------------------------------------------------
# Output parser
# ---------------------------------------------------------------------------

def _parse_radius_stats(output):
    """Parse show radius statistics output."""
    servers = []
    current = None

    field_map = {
        "State": ("state", str),
        "Round Trip Time": ("round_trip_time", int),
        "Access Requests": ("access_requests", int),
        "Access Accepts": ("access_accepts", int),
        "Access Rejects": ("access_rejects", int),
        "Access Challenges": ("access_challenges", int),
        "Retransmissions": ("retransmissions", int),
        "Malformed Responses": ("malformed_responses", int),
        "Bad Authenticators": ("bad_authenticators", int),
        "Pending Requests": ("pending_requests", int),
        "Timeouts": ("timeouts", int),
        "Unknown Types": ("unknown_types", int),
        "Packets Dropped": ("packets_dropped", int),
    }

    for line in output.splitlines():
        m = re.match(r"^\s*RADIUS Server:\s*(.+?):(\d+)\s*$", line)
        if m:
            current = {
                "server": m.group(1).strip(),
                "auth_port": int(m.group(2)),
                "state": "",
                "round_trip_time": 0,
                "access_requests": 0,
                "access_accepts": 0,
                "access_rejects": 0,
                "access_challenges": 0,
                "retransmissions": 0,
                "malformed_responses": 0,
                "bad_authenticators": 0,
                "pending_requests": 0,
                "timeouts": 0,
                "unknown_types": 0,
                "packets_dropped": 0,
            }
            servers.append(current)
            continue

        if current is None:
            continue

        m = re.match(r"^\s*(.+?)\s*:\s*(.+?)\s*$", line)
        if m:
            key = m.group(1).strip()
            value = m.group(2).strip()
            if key in field_map:
                field_name, converter = field_map[key]
                try:
                    current[field_name] = converter(value)
                except (ValueError, TypeError):
                    current[field_name] = value

    return servers


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=True,
    )

    try:
        raw_output = run_command(module, "show radius statistics")
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    servers = _parse_radius_stats(raw_output)
    module.exit_json(changed=False, raw_output=raw_output, servers=servers)


if __name__ == "__main__":
    main()
