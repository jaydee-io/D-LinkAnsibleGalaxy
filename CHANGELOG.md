# Changelog

All notable changes to the `jaydee_io.dlink_dgs1250` Ansible Collection will be documented in this file.

## [0.20.0] - 2026-04-18
### Added
- 3 missing show modules for complete CLI coverage: `show_interfaces_gbic` (§ 30-12), `show_mld_snooping_static_group` (§ 45-16), `show_mld_snooping_statistics` (§ 45-17)
- **591 modules total — full CLI coverage achieved**

### Changed
- Clean up README section headings by removing chapter number prefixes

## [0.19.0] - 2026-04-18
### Added
- All commands from chapters 66–71 (§ 66-1 to 71-7): VRRP, Voice VLAN, Web Authentication, Web-based Access Control — 38 modules

## [0.18.0] - 2026-04-17
### Added
- All commands from chapters 61–65 (§ 61-1 to 65-9): Traffic Control, Traffic Segmentation, Trusted Host, Unit, VLAN — 40 modules

## [0.17.0] - 2026-04-17
### Added
- All commands from chapters 56–60 (§ 56-1 to 60-21): SNTP, Spanning Tree, SSH, SSL, Syslog — 52 modules

## [0.16.0] - 2026-04-17
### Added
- All commands from chapters 51–55 (§ 51-1 to 55-9): Route, Safeguard Engine, Single IP Management, SNMP, SNMPv3 — 56 modules

## [0.15.0] - 2026-04-16
### Added
- All commands from chapters 46–50 (§ 46-1 to 50-4): Port, Port Security, Power Saving, QoS, RMON — 31 modules

## [0.14.0] - 2026-04-15
### Added
- All commands from chapters 41–45 (§ 41-1 to 45-15): MAC Notification, Management, Mirror, MLD Snooping, Multicast Filtering — 55 modules

## [0.13.0] - 2026-04-14
### Added
- All commands from chapters 36–40 (§ 36-1 to 40-6): LACP, Limited IP Multicast, LLDP, Loopback Detection, MAC Address Table — 22 modules

## [0.12.0] - 2026-04-13
### Added
- All commands from chapters 31–35 (§ 31-1 to 35-4): IP-MAC-Port Binding, IPv6 Route, ISM VLAN, Jumbo Frame, L2 Protocol Tunnel — 27 modules

### Fixed
- Workflow permissions for code scanning alerts
- Set package-ecosystem to 'pip' in dependabot config

## [0.11.0] - 2026-04-12
### Added
- All commands from chapters 26–30 (§ 26-1 to 30-11): IGMP, IGMP Snooping, Impersonation Log, Interface, IP — 29 modules

## [0.10.0] - 2026-04-12
### Added
- All commands from chapters 21–25 (§ 21-1 to 25-13): Ethernet OAM, FDB, Firmware, GARP, Gratuitous ARP — 35 modules

## [0.9.0] - 2026-04-11
### Added
- All commands from chapters 16–20 (§ 16-1 to 20-11): CPU, D-Link Discovery Protocol, DHCP Local Relay, DHCP Relay, DHCP Server Screening — 65 modules

## [0.8.0] - 2026-04-10
### Added
- All commands from chapters 13–15 (§ 13-1 to 15-3): Cable Diagnostics, Command Logging, Compound Authentication — 10 modules

## [0.7.0] - 2026-04-09
### Added
- All commands from chapters 10–12 (§ 10-1 to 12-1): BGP, BPDU Protection, Cable Diagnostics — 21 modules

## [0.6.0] - 2026-04-09
### Added
- All commands from chapters 7–9 (§ 7-1 to 9-7): ARP, Authentication, AutoConfig — 37 modules

## [0.5.0] - 2026-04-09
### Added
- ARP Spoofing Prevention commands from chapter 6 (§ 6-1 to 6-2) — 2 modules

## [0.4.0] - 2026-04-09
### Added
- All administration commands from chapter 5 (§ 5-1 to 5-24) — 22 modules

## [0.3.0] - 2026-04-08
### Added
- Initial release on Ansible Galaxy
- System information modules from chapter 2 (§ 2-11 to 2-17) — 7 modules
- All 802.1X commands from chapter 3 (§ 3-1 to 3-16) — 16 modules
- All ACL commands from chapter 4 (§ 4-1 to 4-15) — 15 modules
- Shared `CONNECTION_ARGSPEC` and `connection_from_params` helpers
- Automatic CLI mode management (user/privileged/global config)
- `ansible.netcommon` `network_cli` connection support
- GitHub Actions workflows for unit tests and Galaxy publishing
- `meta/runtime.yml` with `requires_ansible` constraint

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
