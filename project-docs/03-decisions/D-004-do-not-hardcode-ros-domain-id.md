# D-004 · Do not hardcode `ROS_DOMAIN_ID` in `run_tesla_sim.sh`

- **Date:** 2026-09-08
- **Status:** Standing preference of the project owner. **Do not re-propose** without new evidence.

## Context
Teleop commands had no effect because of a domain mismatch, and the
developer's shell profile uses a domain for an unrelated ROS graph whose
generic topic names (`/cmd_vel`) could collide with tesla_sim. Hardcoding a
dedicated domain (e.g. 42) in the run script was proposed.

## Decision
The script inherits whatever `ROS_DOMAIN_ID` the calling shell has. It never
sets or overrides it.

## Why
The owner manages domains per terminal and didn't want a script silently
overriding that. Different team members' setups differ.

## Consequences
- Every terminal used with the sim (teleop, `ros2 topic pub/echo`, other
  packages) must export the same `ROS_DOMAIN_ID`.
- If a crowded domain causes flakiness, pick an unused domain manually and
  export it everywhere. See [08-guides/troubleshooting.md](../08-guides/troubleshooting.md).
- Related: [D-009](D-009-do-not-override-cyclonedds-uri.md).
