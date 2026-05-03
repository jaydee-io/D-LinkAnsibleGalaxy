#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Jérôme Dumesnil
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: dgs1250_config
short_description: Manage configuration sections on a D-Link DGS-1250 switch
description:
  - Manages arbitrary configuration sections on a D-Link DGS-1250 switch.
  - Similar in spirit to C(ios_config) from the Cisco IOS collection.
  - Use this module to push configuration that is not covered by a dedicated
    resource module (e.g. C(dgs1250_vlans), C(dgs1250_l2_interfaces)).
  - Supports parent/child contexts (e.g. C(interface eth1/0/1)), idempotency
    against the running-config, and selective save.
version_added: "1.10.0"
author:
  - Jérôme Dumesnil (@jaydee-io)
extends_documentation_fragment:
  - jaydee_io.dlink_dgs1250.dgs1250
options:
  lines:
    description:
      - Ordered list of configuration commands to push to the switch.
      - Each line is matched against the running-config when C(match=line).
    type: list
    elements: str
  parents:
    description:
      - Ordered list of parent commands that establish the context for
        C(lines) (e.g. C([interface eth1/0/1]) or C([vlan 100])).
      - May also be passed as a single string for convenience.
    type: list
    elements: str
  before:
    description:
      - Ordered list of commands to push before C(lines) (outside of
        C(parents) context).
    type: list
    elements: str
  after:
    description:
      - Ordered list of commands to push after C(lines) (outside of
        C(parents) context, after the implicit C(exit) from C(parents)).
    type: list
    elements: str
  match:
    description:
      - Strategy for matching C(lines) against the running-config.
      - C(line) — only push lines that are not already present (idempotent).
      - C(none) — always push every line, regardless of running-config.
    type: str
    choices: [line, none]
    default: line
  running_config:
    description:
      - Pre-fetched running-config to compare against. Avoids an extra
        C(show running-config) call on the switch.
      - When omitted, the module fetches the running-config itself.
    type: str
  save_when:
    description:
      - When to save running-config to startup-config.
      - C(always) — always save.
      - C(modified) — save only when the module made changes.
      - C(never) — never save.
    type: str
    choices: [always, modified, never]
    default: never
notes:
  - Commands are sent in Global Configuration Mode.
  - When C(parents) is set, an implicit C(exit) is appended after C(lines)
    to leave the parent context.
"""

EXAMPLES = r"""
- name: Configure interface description and shutdown
  jaydee_io.dlink_dgs1250.dgs1250_config:
    parents: interface eth1/0/1
    lines:
      - description Uplink to core
      - shutdown

- name: Configure multiple interfaces
  jaydee_io.dlink_dgs1250.dgs1250_config:
    parents: interface range eth1/0/1-4
    lines:
      - switchport mode access
      - switchport access vlan 100

- name: Push commands and save config when modified
  jaydee_io.dlink_dgs1250.dgs1250_config:
    lines:
      - hostname switch01
      - banner motd ^Authorized access only^
    save_when: modified

- name: Always push lines without idempotency check
  jaydee_io.dlink_dgs1250.dgs1250_config:
    lines:
      - clear logging
    match: none

- name: Use pre-fetched running-config to avoid extra show call
  jaydee_io.dlink_dgs1250.dgs1250_config:
    parents: interface eth1/0/1
    lines:
      - description Server port
    running_config: "{{ lookup('file', 'switch01-running-config.txt') }}"
"""

RETURN = r"""
commands:
  description: List of CLI commands actually sent to the switch.
  returned: always
  type: list
  elements: str
updates:
  description: List of configuration lines that needed to be applied.
  returned: always
  type: list
  elements: str
raw_output:
  description: Raw text output from the switch CLI commands.
  returned: when changed and not in check mode
  type: str
saved:
  description: Whether the running-config was saved to startup-config.
  returned: always
  type: bool
"""

from ansible.module_utils.basic import AnsibleModule

try:
    from ansible_collections.jaydee_io.dlink_dgs1250.plugins.module_utils.dgs1250 import (
        run_commands, get_running_config, MODE_GLOBAL_CONFIG, MODE_PRIVILEGED,
    )
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(
        os.path.dirname(__file__), "..", "module_utils"))
    from dgs1250 import run_commands, get_running_config, MODE_GLOBAL_CONFIG, MODE_PRIVILEGED


# ---------------------------------------------------------------------------
# Running-config section parser
# ---------------------------------------------------------------------------

def _section_lines(running_config, parents):
    """Return the lines under the given parent context in running-config.

    Cisco-style indented config: child lines are indented under their parent.
    Returns a set of stripped lines for membership testing.
    """
    if not running_config:
        return set()
    if not parents:
        return set(line.strip() for line in running_config.splitlines() if line.strip())

    lines = running_config.splitlines()
    in_section = False
    parent_depth = 0
    section = []
    parent_chain = list(parents)
    parent_index = 0

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        indent = len(line) - len(line.lstrip())

        if not in_section:
            if parent_index < len(parent_chain) and stripped == parent_chain[parent_index].strip():
                if parent_index == 0:
                    parent_depth = indent
                parent_index += 1
                if parent_index == len(parent_chain):
                    in_section = True
            elif parent_index > 0 and indent <= parent_depth:
                parent_index = 0
                if stripped == parent_chain[0].strip():
                    parent_depth = indent
                    parent_index = 1
                    if parent_index == len(parent_chain):
                        in_section = True
        else:
            if indent <= parent_depth:
                break
            section.append(stripped)

    return set(section)


# ---------------------------------------------------------------------------
# Command builder
# ---------------------------------------------------------------------------

def _filter_lines(lines, parents, running_config, match):
    """Return the subset of lines that need to be applied.

    With match=none, returns lines as-is.
    With match=line, returns only lines not already present in the section
    of running_config defined by parents.
    """
    if match == "none" or not running_config:
        return list(lines or [])

    section = _section_lines(running_config, parents)
    return [line for line in (lines or []) if line.strip() not in section]


def _build_commands(before, parents, lines_to_apply, after):
    """Assemble the final command list."""
    commands = []
    if before:
        commands.extend(before)
    if parents and lines_to_apply:
        commands.extend(parents)
        commands.extend(lines_to_apply)
        commands.append("exit")
    elif lines_to_apply:
        commands.extend(lines_to_apply)
    if after:
        commands.extend(after)
    return commands


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def _normalize_parents(parents):
    if parents is None:
        return []
    if isinstance(parents, str):
        return [parents]
    return list(parents)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            lines=dict(type="list", elements="str"),
            parents=dict(type="list", elements="str"),
            before=dict(type="list", elements="str"),
            after=dict(type="list", elements="str"),
            match=dict(type="str", choices=["line", "none"], default="line"),
            running_config=dict(type="str"),
            save_when=dict(type="str", choices=[
                "always", "modified", "never"], default="never"),
        ),
        supports_check_mode=True,
    )

    lines = module.params["lines"] or []
    parents = _normalize_parents(module.params["parents"])
    before = module.params["before"] or []
    after = module.params["after"] or []
    match = module.params["match"]
    save_when = module.params["save_when"]
    running_config = module.params["running_config"]

    if not lines and not before and not after:
        module.exit_json(changed=False, commands=[], updates=[], saved=False)
        return

    if match == "line" and lines and running_config is None and not module.check_mode:
        try:
            running_config = get_running_config(module)
        except Exception as e:
            module.fail_json(msg="Failed to fetch running-config: %s" % str(e))

    updates = _filter_lines(lines, parents, running_config, match)
    commands = _build_commands(before, parents, updates, after)

    changed = bool(commands)

    if module._diff and updates:
        diff = {
            'before': '',
            'after': '\n'.join(updates) + '\n',
        }
    else:
        diff = None

    if module.check_mode:
        result = dict(changed=changed, commands=commands,
                      updates=updates, saved=False)
        if diff:
            result['diff'] = diff
        module.exit_json(**result)
        return

    raw_output = ""
    if commands:
        try:
            raw_output = run_commands(module, commands, mode=MODE_GLOBAL_CONFIG)
        except Exception as e:
            module.fail_json(msg="Command failed: %s" % str(e))

    saved = False
    should_save = (save_when == "always") or (
        save_when == "modified" and changed)
    if should_save:
        try:
            run_commands(module, ["copy running-config startup-config"],
                         mode=MODE_PRIVILEGED)
            saved = True
        except Exception as e:
            module.fail_json(msg="Save failed: %s" % str(e))

    result = dict(changed=changed, commands=commands, updates=updates,
                  raw_output=raw_output, saved=saved)
    if diff:
        result['diff'] = diff
    module.exit_json(**result)


if __name__ == "__main__":
    main()
