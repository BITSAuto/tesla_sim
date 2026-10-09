# D-009 · Do not unset or override `CYCLONEDDS_URI` in `run_tesla_sim.sh`

- **Date:** 2026-09-09
- **Status:** Standing preference of the project owner. **Do not re-propose** without new evidence.

## Context
A developer's shell set a custom CycloneDDS config built for an unrelated
multi-machine setup (unicast peers, no multicast). It was a plausible
contributor to the participant-index failures in
[Q-001](../06-open-questions/Q-001-dds-participant-index-failures.md), and
tesla_sim needs no custom DDS config, so unsetting it in the script was
proposed.

## Decision
Same as [D-004](D-004-do-not-hardcode-ros-domain-id.md): the script inherits
whatever the shell provides, including no value.

## Consequences
- If DDS trouble appears, test from a plain shell with no custom
  `CYCLONEDDS_URI`, manually.
- Nodes with different DDS settings can't discover each other, so the sim and
  every terminal talking to it must use the same setting.
