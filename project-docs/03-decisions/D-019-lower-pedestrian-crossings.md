# D-019 · Lower the pedestrian crossings flush with the road

- **Date:** 2026-10-08
- **Status:** Accepted (`de39487`, in [PR #1](https://github.com/BITSAuto/tesla_sim/pull/1))

## Context
The world's two `PedestrianCrossing` nodes are visual-only slabs that sat
about 0.095 m above the road surface. Depth geometry saw that as a step, and
`cart_driver`'s safety monitor fired a false emergency brake at the start
line.

## Decision
Lower both crossings to z = −0.155 so their surface is flush with the road.

## Consequences
- No false obstacle at the start line.
- Related world quirks (intersection surfaces ~10 cm above their collision
  surface) are recorded in [world-geometry.md](../04-knowledge/world-geometry.md)
  and [Q-010](../06-open-questions/Q-010-intersection-surface-offset.md).
