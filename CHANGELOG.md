# Changelog

All notable changes to the `jaydee_io.dlink_dgs1250` Ansible Collection will be documented in this file.

This file is generated from [`changelogs/changelog.yaml`](changelogs/changelog.yaml), the antsibull-changelog source of truth.

## [1.10.0] - 2026-05-03
### Added
- `dgs1250_config` module — a generic configuration module for pushing arbitrary CLI commands with parent/child contexts, idempotency against running-config, and selective save. Similar in spirit to `ios_config`.
- `dgs1250_config` supports `lines`, `parents` (single or list), `before`, `after`, `match` (line/none), `running_config`, and `save_when` (always/modified/never), with section-aware comparison against the running-config.
- `dgs1250_config` supports check_mode and --diff.
- `dgs1250_config` registered in `action_groups` in `meta/runtime.yml`.
- Integration test target for `dgs1250_config` covering idempotency and `match=none` behaviour.
- 20 new unit tests for `dgs1250_config` helpers.

## [1.9.0] - 2026-05-03
### Added
- 12 integration test targets, one per resource module (`dgs1250_vlans`, `dgs1250_l2_interfaces`, `dgs1250_snmp_server`, `dgs1250_logging`, `dgs1250_ntp`, `dgs1250_static_routes`, `dgs1250_acls`, `dgs1250_lag_interfaces`, `dgs1250_storm_control`, `dgs1250_spanning_tree`, `dgs1250_lldp_interfaces`, `dgs1250_dns`).
- 17 integration test targets, one per role (`role_aaa_setup`, `role_acl_setup`, `role_base_config`, `role_dhcp_snooping_setup`, `role_dns_setup`, `role_firmware_upgrade`, `role_hardening`, `role_link_aggregation`, `role_lldp_setup`, `role_monitoring`, `role_ntp_setup`, `role_port_security`, `role_qos_setup`, `role_static_routes_setup`, `role_storm_control_setup`, `role_stp_setup`, `role_vlan_setup`).
- Input validation in all 17 roles via a `validate.yml` task file using `ansible.builtin.assert`, tagged `[validate]` for selective execution with `--tags validate`.
- Extended `integration_config.yml.sample` with safe test values (RFC 5737 TEST-NET-1 IPs, reserved VLAN IDs 3998-3999, test interface, ACL/community/LAG names).
- `firmware_upgrade` and `hardening` role integration tests run in check mode only to avoid reboots and admin lockouts.

## [1.8.0] - 2026-04-26
### Added
- `--diff` support to all 12 resource modules.
- `dgs1250_facts`: `snmp`, `lldp_neighbors`, `stp`, and `static_routes` subsets (11 total).
- `action_groups` in `meta/runtime.yml` and antsibull-changelog configuration.
- 2 example playbooks — `full_monitoring` and `network_baseline`.

## [1.7.0] - 2026-04-26
### Added
- 5 new roles: `stp_setup`, `lldp_setup`, `ntp_setup`, `dns_setup`, `static_routes_setup`.
- `monitoring` role: support for multiple SNMP communities, multiple trap hosts, SNMP traps, multiple syslog servers, RMON.
- 2 example playbooks — `full_monitoring` and `network_baseline`.

## [1.6.0] - 2026-04-26
### Added
- 12 resource modules following the Ansible netcommon pattern (`merged`, `replaced`, `overridden`, `deleted`, `gathered`): `dgs1250_vlans`, `dgs1250_l2_interfaces`, `dgs1250_snmp_server`, `dgs1250_logging`, `dgs1250_ntp`, `dgs1250_static_routes`, `dgs1250_acls`, `dgs1250_lag_interfaces`, `dgs1250_storm_control`, `dgs1250_spanning_tree`, `dgs1250_lldp_interfaces`, `dgs1250_dns`.

## [1.5.0] - 2026-04-25
### Added
- `config_diff` module that compares running-config with startup-config and reports differences.

## [1.4.0] - 2026-04-25
### Added
- All 12 roles now support a `save_config` variable that saves running-config to startup-config after applying changes.

## [1.3.0] - 2026-04-24
### Added
- `show_vlan`: `parsed` return value with VLAN id, name, tagged/untagged ports.
- `show_interfaces_status`: `parsed` return value with status, speed, duplex, type.
- `show_mac_address_table`: `parsed` return value with VLAN, address, type, port.

### Changed
- Extracted shared parsers into `module_utils/dgs1250_parsers.py`.

## [1.2.0] - 2026-04-24
### Added
- `dgs1250_facts`: `interfaces`, `vlans`, and `mac_table` fact subsets.
- All facts exposed via `ansible_facts.dgs1250` following standard network collection pattern.

## [1.1.0] - 2026-04-24
### Added
- 9 new roles for common switch administration tasks: `acl_setup`, `dhcp_snooping_setup`, `firmware_upgrade`, `link_aggregation`, `port_security`, `qos_setup`, `storm_control_setup`, `vlan_setup`, `aaa_setup`.

## [1.0.1] - 2026-04-20
### Fixed
- Add `build_ignore` entries in `galaxy.yml` for `doc`, `.github`, `tests`, `.gitignore`, and `.claude` directories to exclude non-collection files from packaging.

## [1.0.0] - 2026-04-19
### Changed
- **First stable release** — 591 CLI chapter modules, 5 utility modules, 3 roles, 4 example playbooks, integration tests, CI/CD, doc_fragments.
- Add `doc_fragments/dgs1250.py` shared documentation fragment for connection notes.
- Refactor all 591 modules to use `extends_documentation_fragment` reducing documentation duplication.

## [0.21.0] - 2026-04-19
### Added
- 3 ready-to-use roles: `hardening`, `monitoring`, `base_config`.
- 4 example playbooks: initial provisioning, backup/restore, security audit, firmware update.
- Integration tests framework with 3 test targets: `dgs1250_facts`, `dgs1250_mgmt`, `dgs1250_vlan`.

## [0.20.0] - 2026-04-18
### Added
- 3 missing show modules for full CLI reference coverage: `show_interfaces_gbic` (§ 30-12), `show_mld_snooping_static_group` (§ 45-16), `show_mld_snooping_statistics` (§ 45-17).
- **591 modules total — full CLI coverage achieved.**

### Changed
- Clean up README section headings by removing chapter number prefixes.

## [0.19.0] - 2026-04-18
### Added
- All commands from chapters 66–71 (§ 66-1 to 71-7): VRRP, Voice VLAN, Web Authentication, Web-based Access Control — 38 modules.

## [0.18.0] - 2026-04-17
### Added
- All commands from chapters 61–65 (§ 61-1 to 65-9): Traffic Control, Traffic Segmentation, Trusted Host, Unit, VLAN — 46 modules.

## [0.17.0] - 2026-04-17
### Added
- All commands from chapters 56–60 (§ 56-1 to 60-21): SNTP, Spanning Tree, SSH, SSL, Syslog — 52 modules.

## [0.16.0] - 2026-04-17
### Added
- All commands from chapters 51–55 (§ 51-1 to 55-9): Route, Safeguard Engine, Single IP Management, SNMP, SNMPv3 — 56 modules.

## [0.15.0] - 2026-04-16
### Added
- All commands from chapters 46–50 (§ 46-1 to 50-4): Port, Port Security, Power Saving, QoS, RMON — 31 modules.

## [0.14.0] - 2026-04-15
### Added
- All commands from chapters 41–45 (§ 41-1 to 45-15): MAC Notification, Management, Mirror, MLD Snooping, Multicast Filtering — 55 modules.

## [0.13.0] - 2026-04-14
### Added
- All commands from chapters 36–40 (§ 36-1 to 40-6): LACP, Limited IP Multicast, LLDP, Loopback Detection, MAC Address Table — 22 modules.

## [0.12.0] - 2026-04-13
### Added
- All commands from chapters 31–35 (§ 31-1 to 35-4): IP-MAC-Port Binding, IPv6 Route, ISM VLAN, Jumbo Frame, L2 Protocol Tunnel — 27 modules.

### Fixed
- Workflow permissions for code scanning alerts.
- Set package-ecosystem to 'pip' in dependabot config.

## [0.11.0] - 2026-04-12
### Added
- All commands from chapters 26–30 (§ 26-1 to 30-11): IGMP, IGMP Snooping, Impersonation Log, Interface, IP — 29 modules.

## [0.10.0] - 2026-04-12
### Added
- All commands from chapters 21–25 (§ 21-1 to 25-13): Ethernet OAM, FDB, Firmware, GARP, Gratuitous ARP — 35 modules.

## [0.9.0] - 2026-04-11
### Added
- All commands from chapters 16–20 (§ 16-1 to 20-11): CPU, D-Link Discovery Protocol, DHCP Local Relay, DHCP Relay, DHCP Server Screening — 65 modules.

## [0.8.0] - 2026-04-10
### Added
- All commands from chapters 13–15 (§ 13-1 to 15-3): Cable Diagnostics, Command Logging, Compound Authentication — 10 modules.

## [0.7.0] - 2026-04-09
### Added
- All commands from chapters 10–12 (§ 10-1 to 12-1): BGP, BPDU Protection, Cable Diagnostics — 21 modules.

## [0.6.0] - 2026-04-09
### Added
- All commands from chapters 7–9 (§ 7-1 to 9-7): ARP, Authentication, AutoConfig — 37 modules.

## [0.5.0] - 2026-04-09
### Added
- ARP Spoofing Prevention commands from chapter 6 (§ 6-1 to 6-2) — 2 modules.

## [0.4.0] - 2026-04-09
### Added
- All administration commands from chapter 5 (§ 5-1 to 5-24) — 22 modules.

## [0.3.0] - 2026-04-08
### Added
- Initial release on Ansible Galaxy.
- System information modules from chapter 2 (§ 2-11 to 2-17) — 7 modules.
- All 802.1X commands from chapter 3 (§ 3-1 to 3-16) — 16 modules.
- All ACL commands from chapter 4 (§ 4-1 to 4-15) — 15 modules.
- Shared `CONNECTION_ARGSPEC` and `connection_from_params` helpers.
- Automatic CLI mode management (user/privileged/global config).
- `ansible.netcommon` `network_cli` connection support.
- GitHub Actions workflows for unit tests and Galaxy publishing.
- `meta/runtime.yml` with `requires_ansible` constraint.

[1.10.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v1.9.0...v1.10.0
[1.9.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v1.8.0...v1.9.0
[1.8.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v1.7.0...v1.8.0
[1.7.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v1.6.0...v1.7.0
[1.6.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v1.5.0...v1.6.0
[1.5.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v0.21.0...v1.0.0
[0.21.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v0.20.0...v0.21.0
[0.20.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v0.19.0...v0.20.0
[0.19.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v0.18.0...v0.19.0
[0.18.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v0.17.0...v0.18.0
[0.17.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v0.16.0...v0.17.0
[0.16.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v0.15.0...v0.16.0
[0.15.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v0.14.0...v0.15.0
[0.14.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v0.13.0...v0.14.0
[0.13.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v0.12.0...v0.13.0
[0.12.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v0.11.0...v0.12.0
[0.11.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v0.10.0...v0.11.0
[0.10.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v0.7.0...v0.8.0
[0.7.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/jaydee-io/D-LinkAnsibleGalaxy/releases/tag/v0.3.0
