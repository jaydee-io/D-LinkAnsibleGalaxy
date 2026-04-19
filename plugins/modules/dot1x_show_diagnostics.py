#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dot1x_show_diagnostics
short_description: Display 802.1X diagnostics on a D-Link DGS-1250 switch
description:
  - Executes the C(show dot1x diagnostics) CLI command on a D-Link DGS-1250 switch.
  - Returns diagnostic counters for all or specific interface.
  - Corresponds to CLI command described in chapter 3-13 of the DGS-1250 CLI Reference Guide.
version_added: "0.2.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  interface:
    description:
      - Physical port interface to query (e.g. C(eth1/0/1)).
      - If omitted, diagnostics for all interfaces are returned.
    type: str
"""

EXAMPLES = r"""
- name: Get 802.1X diagnostics on port 1
  jaydee_io.dlink_dgs1250.dot1x_show_diagnostics:
    interface: eth1/0/1
  register: diag

- name: Get 802.1X diagnostics on all ports
  jaydee_io.dlink_dgs1250.dot1x_show_diagnostics:
  register: diag_all
"""

RETURN = r"""
raw_output:
  description: Raw text output from the switch CLI command.
  returned: always
  type: str
diagnostics:
  description: List of diagnostic counters per interface.
  returned: success
  type: list
  elements: dict
  contains:
    interface:
      description: Interface name.
      type: str
      sample: "eth1/0/1"
    enters_connecting:
      description: Number of times entering connecting state.
      type: int
    eap_logoffs_while_connecting:
      description: EAP logoffs while connecting.
      type: int
    enters_authenticating:
      description: Number of times entering authenticating state.
      type: int
    successes_while_authenticating:
      description: Successes while authenticating.
      type: int
    timeouts_while_authenticating:
      description: Timeouts while authenticating.
      type: int
    fails_while_authenticating:
      description: Failures while authenticating.
      type: int
    reauths_while_authenticating:
      description: Re-authentications while authenticating.
      type: int
    eap_starts_while_authenticating:
      description: EAP starts while authenticating.
      type: int
    eap_logoffs_while_authenticating:
      description: EAP logoffs while authenticating.
      type: int
    reauths_while_authenticated:
      description: Re-authentications while authenticated.
      type: int
    eap_starts_while_authenticated:
      description: EAP starts while authenticated.
      type: int
    eap_logoffs_while_authenticated:
      description: EAP logoffs while authenticated.
      type: int
    backend_responses:
      description: Backend responses.
      type: int
    backend_access_challenges:
      description: Backend access challenges.
      type: int
    backend_other_requests_to_supplicant:
      description: Backend other requests to supplicant.
      type: int
    backend_non_nak_responses_from_supplicant:
      description: Backend non-NAK responses from supplicant.
      type: int
    backend_auth_successes:
      description: Backend authentication successes.
      type: int
    backend_auth_fails:
      description: Backend authentication failures.
      type: int
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


# ---------------------------------------------------------------------------
# Output parser
# ---------------------------------------------------------------------------

FIELD_MAP = {
    "EntersConnecting": "enters_connecting",
    "EAP-LogoffsWhileConnecting": "eap_logoffs_while_connecting",
    "EntersAuthenticating": "enters_authenticating",
    "SuccessesWhileAuthenticating": "successes_while_authenticating",
    "TimeoutsWhileAuthenticating": "timeouts_while_authenticating",
    "FailsWhileAuthenticating": "fails_while_authenticating",
    "ReauthsWhileAuthenticating": "reauths_while_authenticating",
    "EAP-StartsWhileAuthenticating": "eap_starts_while_authenticating",
    "EAP-LogoffsWhileAuthenticating": "eap_logoffs_while_authenticating",
    "ReauthsWhileAuthenticated": "reauths_while_authenticated",
    "EAP-StartsWhileAuthenticated": "eap_starts_while_authenticated",
    "EAP-LogoffsWhileAuthenticated": "eap_logoffs_while_authenticated",
    "BackendResponses": "backend_responses",
    "BackendAccessChallenges": "backend_access_challenges",
    "BackendOtherRequestsToSupplicant": "backend_other_requests_to_supplicant",
    "BackendNonNakResponsesFromSupplicant": "backend_non_nak_responses_from_supplicant",
    "BackendAuthSuccesses": "backend_auth_successes",
    "BackendAuthFails": "backend_auth_fails",
}


def _new_entry():
    """Return a fresh diagnostics dict with all counters at 0."""
    return {v: 0 for v in FIELD_MAP.values()}


def _parse_diagnostics(output):
    """
    Parse show dot1x diagnostics output.

    Handles single or multiple interface blocks. Each block starts with:
        eth1/0/1 dot1x diagnostic information are following:

    Returns a list of dicts, one per interface.
    """
    results = []
    current = None

    for line in output.splitlines():
        header = re.match(r"^\s*(eth\S+)\s+dot1x diagnostic information", line)
        if header:
            current = _new_entry()
            current["interface"] = header.group(1)
            results.append(current)
            continue

        if current is None:
            continue

        m = re.match(r"^\s*(.+?)\s*:\s*(\d+)\s*$", line)
        if m:
            key = m.group(1).strip()
            if key in FIELD_MAP:
                current[FIELD_MAP[key]] = int(m.group(2))

    return results


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def main():
    module = AnsibleModule(
        argument_spec=dict(
            interface=dict(type="str"),
        ),
        supports_check_mode=True,
    )

    interface = module.params["interface"]

    command = "show dot1x diagnostics"
    if interface:
        command += " interface %s" % interface

    try:
        raw_output = run_command(module, command)
    except Exception as e:
        module.fail_json(msg="Command failed: %s" % str(e))

    result = dict(changed=False, raw_output=raw_output)
    result["diagnostics"] = _parse_diagnostics(raw_output)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
