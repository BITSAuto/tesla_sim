# D-015 · Model the cart's speed behaviour: throttle lag and coast-only slowing

- **Date:** 2026-10-08
- **Status:** Accepted ([PR #1](https://github.com/BITSAuto/tesla_sim/pull/1))

## Context
The cart's brake can't modulate and can damage it, so the team drives at a
fixed 5 km/h with throttle only and stops by releasing throttle and coasting.
The sim used to set wheel velocity to the command instantly, so every stop
was effectively a perfect brake, and coasting couldn't be tested.

## Decision
`tesla_sim/longitudinal.py`: a commanded speed is a throttle setting reached
with a first-order lag (`driveTimeConstant` 1 s); a lower speed or 0 releases
throttle and the car coasts at `coastDecel` (0.4 m/s²), never faster; the
`cmdTimeout` dead-man coasts too.

## Consequences
- The sim now matches what `cart_driver` must cope with.
- `coastDecel` 0.4 m/s² is a **placeholder** until measured on the cart
  ([Q-007](../06-open-questions/Q-007-cart-dimensions-and-coast-rate.md)).
  It sets the emergency-brake threshold in `cart_driver`, so it matters.
