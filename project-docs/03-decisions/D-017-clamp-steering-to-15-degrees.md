# D-017 · Clamp steering to the cart's ±15°

- **Date:** 2026-10-08
- **Status:** Accepted ([PR #1](https://github.com/BITSAuto/tesla_sim/pull/1))

## Context
The Tesla PROTO allows about ±28.6°. The cart's steering lock is ±15°
(`cart_controller`'s `MAX_STEER_DEG`). A planner tuned with 28.6° would plan
turns the cart can't make.

## Decision
New plugin property `maxSteeringDeg` (default 15) clamps commands and the
simulated rack angle.

## Consequences
- With the Tesla's 2.94 m wheelbase, the tightest turn is about 11 m radius.
  The cart's shorter wheelbase should turn tighter
  ([Q-007](../06-open-questions/Q-007-cart-dimensions-and-coast-rate.md)).
- The real cart's exact lock angle is still unmeasured (vehicle_bridge's book).
