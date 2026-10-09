# D-014 · Ship a portable `run_tesla_sim.sh` that also covers native Jazzy and source-built Webots

- **Date:** 2026-10-06
- **Status:** Accepted

## Context
The laptop runs Humble in a distrobox with snap Webots. The Orin runs
Ubuntu 24.04 / Jazzy natively, with Webots built from source in
`$HOME/webots` (there is no arm64 snap).

## Decision
`scripts/run_tesla_sim.sh` detects `WEBOTS_HOME`, the ROS distro and the Qt
plugin path instead of hardcoding them. A Webots build linked against the
system Qt6 gets `QT_PLUGIN_PATH` set automatically, with the multiarch
directory derived so it works on x86_64 and arm64. `TESLA_SIM_WS` overrides
the workspace path.

## Consequences
- One script for both setups. It still sets neither `ROS_DOMAIN_ID` nor
  `CYCLONEDDS_URI` ([D-004](D-004-do-not-hardcode-ros-domain-id.md),
  [D-009](D-009-do-not-override-cyclonedds-uri.md)).
